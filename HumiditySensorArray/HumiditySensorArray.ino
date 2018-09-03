const int SENSOR_SIZE = 4;
const int SAMPLES = 100;
int values[SENSOR_SIZE][SAMPLES];

void setup() {
  Serial.begin(9600);
  // Power PIN
  pinMode(12, OUTPUT);
  digitalWrite(12, LOW);
}

void loop() {
  long start = millis();

  digitalWrite(12, HIGH);
  delay(10);
  for(int i = 0; i < SENSOR_SIZE; i++) {
    for(int j = 0; j < SAMPLES; j++) {
      values[i][j] = analogRead(i);
    }
  }
  delay(10);
  digitalWrite(12, LOW);

  Serial.print("START,");

  for(int i = 0; i < SENSOR_SIZE; i++) {
    long accum = 0;

    for(int j = 0; j < SAMPLES; j++) {
      accum += values[i][j];
    }

    Serial.print(accum / (float) SAMPLES);

    if(i != (SENSOR_SIZE -1)) {
      Serial.print(",");
    } else {
      Serial.print("\n");
    }
  }

  delay(1000 - (millis() - start));
}