#include WiFi
#define BUTTON_1 13
#define	BUTTON_2 12
#define BUTTON_3 14
#define BUTTON_4 27
 
//connect to iphone hotspot
const char* ssid = "Iphone"
const char* password = "password"

//light stuff
const byte ledPins[] = {15, 2, 4};	//red, green, blue
const byte chns[] = {0, 1, 2};		//pwm channels
int red, green, blue

//HTTP Request Shite
int HTTP_PORT = 5000;
string HTTP_METHOD = "GET";
char HOST_NAME[] = "http://127.0.0.1:5000/"
string PATH_1 = "/Apples123"

void connectToNetwork() {
	
	WiFi.begin(ssid, password);
	
	while (WiFi.status() != WL_CONNECTED) {
		delay(1000);
		Serial.println("Connecting to WiFi...");
	}

	Serial.println("Connected to Network");

}

void setup() {
	
	pinMode(BUTTON_1, INPUT)
	pinMode(BUTTON_2, INPUT)
	pinMode(BUTTON_3, INPUT)
	pinMode(BUTTON_4, INPUT)

	connectToNetwork();

	for(int i = 0; i < 3; i++) {
		ledcSetup(chns[i], 1000, 8);
		ledcAttachPin(ledPins[i], chns[i]);
	}

	
	
}

void loop() {

	if(digitalRead(BUTTON_1) == HIGH):
		Serial.println("Button 1")
	
	else if(digitalRead(BUTTON_2) == HIGH):
		Serial.println("Button 2")
	
	else if(digitalRead(BUTTON_3) == HIGH):
		Serial.println("Button 3")
	
	else if(digitalRead(BUTTON_4) == HIGH):
		Serial.println("Button 1")
	
		
}

void send_order() {
	if(client.connect(HOST_NAME, HTTP_PORT)){
		Serial.println("Connected to Server");

		//send request header
		client.println(HTTP_METHOD + " " + PATH_NAME + " HTTP/1.1");
		client.println("Host: " + String(HOST_NAME));
		client.println("Connection: close");
		client.println();

		while(clien.available()) {
			//read bytes
			char c = client.read();
			Serial.print(c);
		}

	} else {
		Serial.println("Connection Failed");
	}

}

void check_status() {

}
	
void setColor(int b) {
	if(b == 0):
		ledcWrite(chns[0], 255);		
		ledcWrite(chns[1], 0);		
		ledcWrite(chns[2], 0);		
	
	else if(b == 1):
		ledcWrite(chns[0], 0);		
		ledcWrite(chns[1], 255);		
		ledcWrite(chns[2], 0);		
	
	else if(b == 2):
		ledcWrite(chns[0], 0);		
		ledcWrite(chns[1], 0);		
		ledcWrite(chns[2], 255);		
	
