/* Software del Microcontrolador Nano Arduino
permite el control del sistema 1v de desinfección
ultravioleta */


//Librerias usadas

#include <Wire.h>
#include <RTClib.h>
#include <SD.h>
#include <SPI.h>

RTC_DS3231 rtc;
File myFile; 
Sd2Card card;
SdVolume volume;
SdFile root;

//Variables usadas 

int btn = 5;
int LED = 6;
int UV = 7;
int stop = 2;
volatile int ax = 0;
volatile int flag;

const int chipSelect = 4;

void setup()
{
  //configuración de la comunicación serial
  Serial.begin(9600);
  delay(5);
  Serial.println("Setup....");
  // Chequeando el SD Card
  if (!card.init(SPI_HALF_SPEED, chipSelect)) 
    {
        Serial.println("Inicialización de la tarjeta SD contiene ERROR");
        Serial.println("*Esta la tarjeta SD ingresada?");
      }
    else 
      {
        Serial.println("Todo correcto. Arrancando SD...");
      }



    if (!SD.begin(4)) 
      {
       Serial.println("Se desactivan registros, error al cargar SD");
      }
    else
      {
        Serial.println("inicializacion exitosa del SD");
        Serial.print("Consultando archivos de almacenamiento 0 no existe 1 si existe:  ");
        Serial.println(SD.exists("datalog.csv"));
        // Checando si el SD es nuevo o formateado
        if(!SD.exists("DATALOG.csv"))
          {
            myFile = SD.open("datalog.csv", FILE_WRITE);
            Serial.println("Archivo nuevo, Escribiendo encabezado(fila 1)");
            myFile.println("Fecha en DD/MM/AA,Hora:Minuto,Estado");
            myFile.close();
           } 
        else 
           {
             Serial.println("Archivo reconocido, SD configurada anteriormente");
           }
      }
    // Chequeando el modulo reloj

    if (!rtc.begin()) 
     {
      Serial.println("Error módulo RTC");
     }
    else
     {
      Serial.println("Módulo reloj funcionando");
     }

   //El led  alerta 
   pinMode(LED, OUTPUT);
    //El pin BTN
   pinMode(btn,INPUT);
   //Pin Interrupcion STOP
     pinMode(stop, INPUT_PULLUP);
     attachInterrupt(digitalPinToInterrupt(stop), blink, CHANGE);
    //El rele de la luz UV SET OFF POR SEGURIDAD SIEMPRE
     pinMode(UV,OUTPUT);
     digitalWrite(UV,LOW);

     Serial.println("Setup completado, Listo.");
}


void blink()  //La funcion de interrupcion 
{
  ax=0;
  flag=2;
  digitalWrite(LED,LOW);
  digitalWrite(UV,LOW);
}

void loop()
{
    digitalWrite(UV,LOW);   //Siempre se setea a OFF por seguridad. SIEMPRE
    digitalWrite(LED,LOW);
    
    ax=2;    //ax es una variable volatil (cambia en la interrupción)
           //que funciona como un flag de stop de  emergencia.
    flag =1;
    Serial.println("ONLINE");
    while(flag==1)
    {

    if(digitalRead(btn)==HIGH)   //Todo el tiempo consulta si el btn es presionado
        //y solo ejecuta el esterilizamiento y registro 
        //si btn es presionado. 
		{
    //Lo primero que realiza es señalar que el sistema empieza a arrancar
    //durante 10 segundos con un aviso visual de un led de alto brillo.
        	Serial.println("Iniciando protocolo de esterilizacion");
        	for (int i = 0; i <= 8; i++)  //PARAPADEO
          	{
            	digitalWrite(LED, HIGH);
            	delay(1000-125*i);
            	digitalWrite(LED,LOW);
            	delay(1000-125*i);
          	}

          	DateTime now = rtc.now();

        	float aux = now.minute();
        	float aux1 = now.hour();
        	float horas = aux1 + aux/60;
  
        	DateTime now1 = rtc.now();
        	float auxi = now1.minute();
        	float auxi1 = now1.hour();
        	float horasi = auxi1 + auxi/60;
        	digitalWrite(UV,HIGH);
        	digitalWrite(LED,HIGH);

        	while(horasi-horas<0.03 && ax>1)
            	{
              		DateTime now2 = rtc.now();
              		float auxii = now2.minute();
              		float auxii1 = now2.hour();
              		horasi = auxii1 + auxii/60; 
            	} 


	    	if(ax==2)
    	   		{
            		Serial.println("ESTERILIZADO COMPLETEADO");
            		digitalWrite(UV,LOW);
    				digitalWrite(LED,LOW); //POR SEGURIDAD SE VUELVEN A SET CERO);
            		DateTime now = rtc.now();
         			myFile = SD.open("DATALOG.csv", FILE_WRITE);//abrimos  el archivo
          			if(myFile)
        	  		{
          				Serial.println("Guardando info en SD: protocolo COMPLETADO");  
          				myFile.print(now.day());
          				myFile.print('/');
          				myFile.print(now.month());
          				myFile.print('/');
          				myFile.print(now.year());
          				myFile.print(",");
          				myFile.print(now.hour());
          				myFile.print(':');
          				myFile.print(now.minute());
          				myFile.print(':');
          				myFile.print(now.second()); 
          				myFile.print(",");
          				myFile.println("Completado"); 
          				myFile.close();   
              		}
        		}

        	else if(ax==0)
        		{
            		Serial.println("INTERRUPCION!!");
            		DateTime now = rtc.now();
          			myFile = SD.open("DATALOG.csv", FILE_WRITE);//abrimos  el archivo
          			if(myFile)
          			{
          				Serial.println("Guardando info en SD: protocolo NO COMPLETADO");  
          				myFile.print(now.day());
          				myFile.print('/');
          				myFile.print(now.month());
          				myFile.print('/');
          				myFile.print(now.year());
          				myFile.print(",");
          				myFile.print(now.hour());
          				myFile.print(':');
          				myFile.print(now.minute());
          				myFile.print(':');
          				myFile.print(now.second()); 
          				myFile.print(",");
          				myFile.println("Se interrumpio la Esterilizacion"); 
          				myFile.close(); 
            		}
            	}
        }
    }

    Serial.println("Volviendo al sistema ONLINE...");
    digitalWrite(UV,LOW);
    digitalWrite(LED,LOW); //POR SEGURIDAD SE VUELVEN A SET CERO);
	delay(10);
    }
    
   

	








