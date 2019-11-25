#include <avr/io.h>
#include <stdio.h>

#define F_CPU 8000000UL
#include <util/delay.h>

#include "lab_uino.h"
#include "lcd_usb.h"
#include "funcoes.h"

void blinkLedsSequence();
void blinkLeds();
void auxBlinkLeds(char);
void blindLedsEvenOdd();
void auxBlindLedsEvenOdd(char, char);

char checkPin(int);
void sleep(int);
void turnOnOffLed(unsigned char, char);

///////////////////////////////////////////

// PINS: ACK (7), BUSY(8), ERROR(4)
const int pin1 = 7;
const int pin2 = 8;
const int pin3 = 4;

int main() {
	IO_init();
	
	while (1) {
		if (Ch_ack_lig)
			blinkLeds();
		else if (Ch_busy_lig)
			blindLedsEvenOdd();
		else if (Ch_error_lig)
			blinkLedsSequence();
	}
}

///////////////////////////////////////////

unsigned char numberOfLeds = 14;

#define sleepTimeSequence 250
void blinkLedsSequence() {
	for (unsigned char led=1; led<=numberOfLeds; led++) {
		turnOnOffLed(led, 1);
		_delay_ms(sleepTimeSequence);
		turnOnOffLed(led, 0);
	}
}

#define sleepTimeEvenOdd 250
#define overallTimeEvenOdd 3000
void blindLedsEvenOdd() {
	float timePassedSeconds = 0;
	char even = 1;
	while (timePassedSeconds < overallTimeEvenOdd) {
		auxBlindLedsEvenOdd(even, 1);
		auxBlindLedsEvenOdd(even, 0);
		even = !even;
		timePassedSeconds += 2*sleepTimeEvenOdd;
	}
}
void auxBlindLedsEvenOdd(char even, char ledsOn) {
	for (unsigned char led=1; led<=numberOfLeds; led++)
		if ((led%2==0)==even)
			turnOnOffLed(led, ledsOn);
	_delay_ms(sleepTimeEvenOdd);
}

#define sleepTimeSimple 500
#define overallTimeSimple 3000
void blinkLeds() {
	float timePassedSeconds = 0;
	while (timePassedSeconds < overallTimeSimple) {
		auxBlinkLeds(1);
		auxBlinkLeds(0);
		timePassedSeconds += 2*sleepTimeSimple;
	}
}
void auxBlinkLeds(char ledsOn) {
	for (unsigned char led=1; led<=numberOfLeds; led++)
		turnOnOffLed(led, ledsOn);
	_delay_ms(sleepTimeSimple);
}

///////////////////////////////////////////

void turnOnOffLed(unsigned char number, char on) {
	if (on)
		led_on(number);
	else
		led_off(number);
}