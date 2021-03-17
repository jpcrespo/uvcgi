// Librería para la comunicación I2C y la RTClib
#include <Wire.h>
#include <RTClib.h>
 
// Declaramos un RTC DS3231
RTC_DS3231 rtc;
 
void setup () 
{
	Serial.begin(9600);
 	delay(3000);
 // Comprobamos si tenemos el RTC conectado
 	if (!rtc.begin())
 	{
		Serial.println("No hay un módulo RTC");
 	}
 
 // Ponemos en hora, solo la primera vez, luego comentar y volver a cargar.
 // Ponemos en hora con los valores de la fecha y la hora en que el sketch ha sido compilado.
 	//rtc.adjust(DateTime(2021,1,17,16,52));
}


void loop () {


 DateTime now = rtc.now();
 
 Serial.print(now.day());
 Serial.print('/');
 Serial.print(now.month());
 Serial.print('/');
 Serial.print(now.year());
 Serial.print(" ");
 Serial.print(now.hour());
 Serial.print(':');
 Serial.print(now.minute());
 Serial.print(':');
 Serial.print(now.second());
 Serial.println(now.unixtime());
 delay(3000);

}
