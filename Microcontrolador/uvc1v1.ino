/* Software del Microcontrolador Nano Arduino
permite el control del sistema 1v de desinfección
ultravioleta */


//Librerias usadas SD, RTC 
#include <SD.h>
#include <Wire.h>
#include <RTClib.h>
//#include <SPI.h>


//definiciones e inicializaciones
RTC_DS3231 rtc;
File myFile; 
Sd2Card card;
SdVolume volume;
SdFile root;


int btn = 5;           //Boton para Activar sistema
int LED = 6;       //Led de aviso
int UV = 7;        //Control Activador UV
int stop = 2; //BOTON DE EMERGENCIA


int d,m,a,h1,m1,s1=0;


volatile int ax=2; //Controlador de estados
const int chipSelect = 4;  //Control SD


void setup()
{
  //configuración de la comunicación serial
  Serial.begin(9600);
  Serial.println("Setup.... Serial ok.");
  if (!SD.begin(4)) 
      {
       Serial.println("Se desactivan registros, Modulo SD no encontrado");
      }
  else if(!card.init(SPI_HALF_SPEED, chipSelect)) 
  {
      Serial.println("Inicialización de la tarjeta SD contiene ERROR");
        Serial.println("*Esta la tarjeta SD ingresada?");
    }
    else 
    {
      Serial.println("Modulo SD... ok");
        Serial.println("Tarjeta SD... ok");
        Serial.println("Buscando Archivo Log...");
        if(!SD.exists("datalog.csv"))
          {
            myFile = SD.open("datalog.csv", FILE_WRITE);
            Serial.println("Creando Archivo nuevo, Escribiendo encabezado(fila 1)");
            myFile.println("Fecha en DD/MM/AA,Hora Inicio,Estado");
            myFile.close();
           } 
        else 
           {
             Serial.println("Archivo reconocido, SD configurada anteriormente");
           }
    }


    if (!rtc.begin()) 
     {
      Serial.println("Error módulo RTC");
     }
    else
     {
      Serial.println("Módulo reloj ...ok");
     }

   //El led  alerta 
    pinMode(LED, OUTPUT);
    //El pin BTN
    pinMode(btn,INPUT_PULLUP);
   //Pin Interrupcion STOP
    pinMode(stop, INPUT_PULLUP);   
    attachInterrupt(digitalPinToInterrupt(stop), blink, FALLING);
    //El rele de la luz UV SET OFF POR SEGURIDAD SIEMPRE
    pinMode(UV,OUTPUT);
    digitalWrite(UV,LOW);
    pinMode(10,OUTPUT);           //Led que indica SISTEMA ONLINE
    digitalWrite(10,HIGH);
    Serial.println("Setup completado, Listo.");
    Serial.println("ONLINE");
}


void registrar()
{
  digitalWrite(UV,LOW);
  digitalWrite(LED,LOW);
  digitalWrite(10,LOW);

  myFile = SD.open("datalog.csv", FILE_WRITE);//abrimos  el archivo
  if(myFile)
    {
      Serial.println("Escribiendo en tarjeta SD");
      myFile.print(d);
      myFile.print('/');
      myFile.print(m);
      myFile.print('/');
      myFile.print(a);
      myFile.print(",");
      myFile.print(h1);
      myFile.print(':');
      myFile.print(m1);
      myFile.print(':');
      myFile.print(s1); 
      myFile.print(",");
      myFile.println("COMPLETADO");
      myFile.close();
    }
        
  else
  {
    Serial.println("Error al escribir dato");
  } 

}


void blink()
{
  ax=0;
  digitalWrite(LED,LOW);
  digitalWrite(UV,LOW);
  digitalWrite(10,LOW);
}


void loop()
{ 
    ax=2;
    digitalWrite(UV,LOW);   //Siempre se setea a OFF por seguridad. SIEMPRE
    digitalWrite(LED,LOW);
    digitalWrite(10,HIGH);

    while(digitalRead(btn)==LOW)   //Todo el tiempo consulta si el btn es presionado
        //y solo ejecuta el esterilizamiento y registro 
        //si btn es presionado. 
  {
    //Lo primero que realiza es señalar que el sistema empieza a arrancar
    //durante 10 segundos con un aviso visual de un led de alto brillo.
        Serial.println("Iniciando protocolo");
    
        digitalWrite(LED,HIGH);
        delay(5000);
        digitalWrite(LED,LOW);
        delay(500);
        digitalWrite(UV,HIGH);
        delay(15);
        digitalWrite(LED,HIGH);
        delay(5);
        DateTime now = rtc.now();

        d = now.day();
        m = now.month();
        a = now.year();
        h1 = now.hour();
        m1 = now.minute();
        s1 = now.second();

        int hr0=now.unixtime();
        DateTime now1 = rtc.now();
        int hr1=now1.unixtime();
    
        while(ax>1)
        {
          while(hr1-hr0<=10 && ax>1)
          {
            DateTime now1=rtc.now();
            hr1=now1.unixtime();
            delay(3000);
          }
          if(ax==2)
          {
            Serial.println("ESTERILIZADO COMPLETEADO");
            registrar();
            ax=0;
          }
          else if(ax==0)
          {
            Serial.println("STOP");
          }

        }
        delay(100);
    }
  ax=2;
}