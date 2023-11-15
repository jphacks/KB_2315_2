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

#include <secret.h>

#define DHT1 27
#define DHT2 19
#define DHTTYPE DHT22 // DHT 22 (AM2302)

AsyncWebServer server(80);

StaticJsonDocument<288> json_doc;
HTTPClient http_session;
HTTPClient http_sensor;
SHT3X unitsht30;
QMP6988 unitqmp6988;
UNIT_HBRIDGE driver;

DHT_Unified dht1(DHT1, DHTTYPE);
DHT_Unified dht2(DHT2, DHTTYPE);

const int update_interval_sec = 2;

bool drying = false;

long long timer = 0;

float RoomTemp, RoomHumi, ShoeTemp, ShoeHumi, ShoePre, Shoe2Temp, Shoe2Humi;

int debug_flag = 0;

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
    char exporter_plain_json[1536];
    serializeJson(json_doc, exporter_plain_json, sizeof(exporter_plain_json));

    request->send(200, "application/json", exporter_plain_json);
  });

  // サーバーの開始
  server.begin();
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
                      ",\"humidity\":" + String(Shoe2Temp) + "}";
}

void loop() {
  if (millis() - timer > update_interval_sec * 1000) {
    timer = millis();

    Serial.println(WiFi.localIP());

    scan();
  }
}