#include <ArduinoJson.h>

int x, y, r;

void setup() {
  Serial.begin(9600); 
}

void loop() {
  //Envia o pedido das coordenadas
  Serial.println("get");
  
  //Espera receber resposta
  while(!Serial.available()){
  }

  //Lê o json com o circulo
  String json = Serial.readString();
  
  Serial.print("Arduino : ");
  Serial.println(json);
  
  //Inicializa o buffer do json
  DynamicJsonDocument doc(1024);

  //Desemcapsula o json
  DeserializationError error = deserializeJson(doc, json);
  
  //Tratamento de erro pra deserialização
  if (error) {
      Serial.print(F("Falha ao deserializar JSON: "));
      Serial.println(error.f_str());
      return;
  }

  x = doc["x"];
  y = doc["y"];
  r = doc["r"];
  String s = doc["s"];

  Serial.print("Arduino : X:");
  Serial.print(x);
  Serial.print("; Y:");
  Serial.print(y);
  Serial.print("; R:");
  Serial.print(r);
  Serial.print("; S:");
  Serial.println(s);
}
