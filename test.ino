



void setup() {
    Serial.begin(9600);
    pinMode(2,OUTPUT); //thumb
    pinMode(3, OUTPUT); //pointer
    pinMode(4, OUTPUT); //middle
    pinMode(5, OUTPUT); //ring
    pinMode(6, OUTPUT); //pinky

}

void loop() {
    if (Serial.available()){
        String command = Serial.readStringUntil('\n');
        command.trim();
        int counter = 2;
        for (int i : command){
            if (i == '1'){//on
                digitalWrite(counter, HIGH);
            } else { //off
                digitalWrite(counter, LOW);
            }
            counter++;
        }


    }
}
