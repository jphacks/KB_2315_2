#include <Adafruit_Sensor.h>
#include <Arduino.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ESPAsyncWebServer.h>
#include <HTTPClient.h>
#include <M5Core2.h>

#include "M5_ENV.h"
#include "UNIT_HBRIDGE.h"

#include <config.h>
#include <secret.h>

#define DHT1 27
#define DHT2 19
#define DHTTYPE DHT22 // DHT 22 (AM2302)

AsyncWebServer server(80);

StaticJsonDocument<384> json_doc;
HTTPClient http_session;
HTTPClient http_sensor;
SHT3X unitsht30;
QMP6988 unitqmp6988;
UNIT_HBRIDGE driver;

DHT_Unified dht1(DHT1, DHTTYPE);
DHT_Unified dht2(DHT2, DHTTYPE);

const int update_interval_sec = 10;

bool drying = false;

long long timer = 0;

float RoomTemp, RoomHumi, ShoeTemp, ShoeHumi, ShoePre, Shoe2Temp, Shoe2Humi;

int debug_flag = 0;
float volt = 0.0; //デバッグ用
void setup() {

  M5.begin();
  Serial.begin(115200);
  Wire.begin(32, 33); // Wire init, adding the I2C bus.  Wire初始化, 加入i2c总线
  pinMode(14, OUTPUT);
  digitalWrite(14, HIGH);

  dht1.begin();
  dht2.begin();
  unitsht30.init(0x44, &Wire);
  unitqmp6988.init(QMP6988_SLAVE_ADDRESS_H, &Wire);
  driver.begin(&Wire, HBRIDGE_ADDR, 32, 33, 100000L);

  // WiFi Setup

#if STATIC_IP
  WiFi.config(ip, gateway, subnet);
#endif

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    M5.Lcd.fillScreen(BLACK);               // 画面の塗りつぶし
    M5.Lcd.setCursor(0, 0);                 // 文字列の書き出し位置
    M5.Lcd.setTextSize(1);                  // 文字サイズを設定
    M5.Lcd.printf("Connecting to WiFi..."); // シリアルモニタ
  }

  M5.Lcd.fillScreen(BLACK);      // 画面の塗りつぶし
  M5.Lcd.setCursor(0, 0);        // 文字列の書き出し位置
  M5.Lcd.setTextSize(1);         // 文字サイズを設定
  M5.Lcd.printf("WiFi Success"); // シリアルモニタ
  // リクエストに応じてJSON形式のデータを返すエンドポイントの設定
  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request) {
    char exporter_plain_json[3072];
    serializeJson(json_doc, exporter_plain_json, sizeof(exporter_plain_json));

    request->send(200, "application/json", exporter_plain_json);
  });

  // サーバーの開始
  server.begin();
}

int drying_status(){

  if(abs(ShoeTemp - RoomTemp) > GAP_TEMP){
    
    if((ShoeHumi - RoomHumi) > GAP_HUM) {
      return 1;
    }
    else{
      return 2;
    }
  } else {
    return 0;
  }  
}

void main_func() {
  int current_drying = drying_status();

  if (drying) { // 乾燥実行中
    if (current_drying == 1) {
      // 靴が湿気ている
      //追い出し続行
      driver.setDriverDirection(1);
      driver.setDriverSpeed8Bits(255);
    }else if (current_drying == 2) {
      //湿度は低いが熱を持っている
      //外気温と平衡にさせる
      driver.setDriverDirection(1);
      driver.setDriverSpeed8Bits(128);
    }else {
      // 靴が湿気ていない
      //乾燥終了
      driver.setDriverDirection(0);
      driver.setDriverSpeed8Bits(0);
      drying = false;
    }
  } else { // 乾燥未実行
    if (current_drying==1) {
      // 靴が湿気ている
      //乾燥開始
      driver.setDriverDirection(1);
      driver.setDriverSpeed8Bits(255);
      drying = true;
    }
    else{
      driver.setDriverDirection(0);
      driver.setDriverSpeed8Bits(0);   
    }
  }

}

void scan() {
  sensors_event_t event;
  dht1.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  } else {
    RoomTemp = event.temperature;
  }
  // Get humidity event and print its value.
  dht1.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  } else {
    RoomHumi = event.relative_humidity;
  }

  // DHT2
  dht2.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  } else {
    Shoe2Temp = event.temperature;
  }
  // Get humidity event and print its value.
  dht2.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  } else {
    Shoe2Humi = event.relative_humidity;
  }

  // Unitが室内環境計測
  ShoePre = unitqmp6988.calcPressure();
  if (unitsht30.get() == 0) { // 温湿度取得
    ShoeTemp = unitsht30.cTemp;
    ShoeHumi = unitsht30.humidity;
  } else { // 温湿度取れない場合は気圧もクリア
    ShoeTemp = 0, ShoeHumi = 0, ShoePre = 0;
  }

  json_doc["Room"] = "{\"temperature\":" + String(RoomTemp) +
                     ",\"humidity\":" + String(RoomHumi) + "}";
  json_doc["Shoe"] = "{\"temperature\":" + String(ShoeTemp) +
                     ",\"humidity\":" + String(ShoeHumi) +
                     ",\"pressure\":" + String(ShoePre) + "}";
  json_doc["Shoe2"] = "{\"temperature\":" + String(Shoe2Temp) +
                      ",\"humidity\":" + String(Shoe2Humi) + "}";

  M5.Lcd.setRotation(3);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setCursor(0, 20);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setTextColor(WHITE, BLACK);  
  volt = driver.getAnalogInput(_12bit) / 4095.0f * 3.3f / 0.09f;
  M5.Lcd.printf("Room T:%2.1f, H:%2.0f%%\r\n",
                RoomTemp, RoomHumi);
  M5.Lcd.printf("Shoe T:%2.1f, H:%2.0f%%, P:%2.0fPa\r\n",
                ShoeTemp, ShoeHumi, ShoePre);
  M5.Lcd.printf("Shoe2 T:%2.1f, H:%2.0f%%\r\n",
                Shoe2Temp, Shoe2Humi);
  M5.Lcd.printf("Voltage:%.2fV\r\n", volt);
  M5.Lcd.printf("%s",WiFi.localIP().toString().c_str());
}

void loop() {
  if (millis() - timer > update_interval_sec * 1000) {
    timer = millis();

    Serial.println(WiFi.localIP());
    json_doc.clear();
    scan();

    main_func();

  }
}