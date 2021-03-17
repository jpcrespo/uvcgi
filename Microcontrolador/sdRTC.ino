#include <SD.h>
#include <Wire.h>
#include <RTClib.h>

File myFile;
RTC_DS3231 rtc;




void setup()
{

  if (!rtc.begin())
  {
    Serial.println("No hay un módulo RTC");
  }

  
  Serial.begin(9600);
  Serial.print("Iniciando SD ...");
  if (!SD.begin(4)) {
    Serial.println("No se pudo inicializar");
    return;
  }
  Serial.println("inicializacion exitosa");
  
  if(!SD.exists("datalog.csv"))
  {
      myFile = SD.open("datalog.csv", FILE_WRITE);
      if (myFile) {
        Serial.println("Archivo nuevo, Escribiendo encabezado(fila 1)");
        myFile.println("Tiempo(ms),Sensor1,Sensor2,Sensor3");
        myFile.close();
      } else {

        Serial.println("Error creando el archivo datalog.csv");
      }
  }
  
}

void loop()
{
  myFile = SD.open("datalog.csv", FILE_WRITE);//abrimos  el archivo
  
  if (myFile) { 
 DateTime now = rtc.now();
 
 myFile.print(now.day());
 myFile.print('/');
 myFile.print(now.month());
 myFile.print('/');
 myFile.print(now.year());
 myFile.print(" ");
 myFile.print(now.hour());
 myFile.print(':');
 myFile.print(now.minute());
 myFile.print(':');
 myFile.println(now.second());   
 Serial.println(now.unixtime());      
 myFile.close()              
  
  } else {
  	// if the file didn't open, print an error:
    Serial.println("Error al abrir el archivo");
  }
  delay(100);
}