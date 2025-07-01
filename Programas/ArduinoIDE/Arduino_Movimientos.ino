#include <Arduino.h>
#include <Servo.h>

// Articulaciones del brazo
enum Articulacion {
  BASE,
  HOMBRO,
  CODO,
  MUNHECA_ROT,
  MUNHECA_IN,
  PINZA
};

// String para mandar un mensaje al arduino mediante el Serial Monitor. Permite hacer movimientos del brazo sin escribir una función
// completa. Sirve para pruebas. Comando no necesariamente tiene el mismo nombre que la función a la que llama
String comando;

// Arreglo de 6 servos, uno para cada articulación
Servo servos[6];    // servos[BASE], servos[HOMBRO] , servos[CODO] , servos[MUNHECA_ROT], servos[MUNHECA_IN], servos[PINZA]

// Posición inicial donde el brazo está seguro sin golpear nada. 
const int home[6] = {
  105,  // BASE
   35,  // HOMBRO
   5,  // CODO
   80,  // MUNHECA_ROT
  160,  // MUNHECA_IN
   70   // PINZA
};

// Posiciones alternativas
const int posicion_1[6] = {80, 70, 7, 80, 160, 0};     // Posición 1: Posición para iniciar el movimiento

void mover_servos_posicion(const int destino[6]);
void mover(Articulacion articulacion, int destino);
bool parsear_comando(const String& mensaje, String &nombre, int &angulo);
bool nombre_a_articulacion(const String& nombre, Articulacion& resultado);
void agarrar_caja();
void zona_vencido();
void zona_no_vencido();
void suave(Articulacion articulacion, int inicio, int final);
void circuito1();
void circuito2();
void HOME();

void subir();

void setup() {
  servos[BASE].attach(2);     //Base al Pin digital 1 (Conexión protoboard)
  servos[HOMBRO].attach(3);
  servos[CODO].attach(4);
  servos[MUNHECA_ROT].attach(5);
  servos[MUNHECA_IN].attach(6);
  servos[PINZA].attach(10);
  
  Serial.begin(9600);

  // Posición inicial
  mover_servos_posicion(home);
  delay(2000);                

  Serial.println("READY");    
}

void loop() {
  if (Serial.available() > 0) {
    comando = Serial.readStringUntil('\n');
    comando.trim(); 

    String nombre;
    int angulo;

    if (parsear_comando(comando, nombre, angulo)) {
      Articulacion articulacion;
      if (nombre_a_articulacion(nombre, articulacion)) {
        mover(articulacion, angulo);
        Serial.println("OK");
      } else {
        Serial.println("ERROR: Articulación no válida");
      }
      return;
    }

    // --- Comandos de posición predeterminada ---
    // Si deseas agregar un mensaje para que haga un movimiento el brazo, agregalo aqui
    if (comando == "POS1") mover_servos_posicion(posicion_1);
    else if (comando == "CAJA") agarrar_caja();
    else if (comando == "VENCIDO") zona_vencido();
    else if (comando == "NO_VENCIDO") zona_no_vencido();
    else if(comando == "SUBIR") subir();
    else if(comando == "CIRCUITO1") circuito1();
    else if(comando == "CIRCUITO2") circuito2();
    else if(comando=="HOME") HOME();
    else {
      Serial.println("ERROR: Comando no reconocido");
      return;
    }

    Serial.println("OK");
  }
}

//==========codigo Brazo-Robot final=============
//===============================================

void HOME(){
  mover(BASE, 105);
  mover(PINZA, 70);
  mover(CODO, 5);
  mover(MUNHECA_ROT, 80);
  mover(MUNHECA_IN, 160);
}

void suave(Articulacion articulacion, int inicio, int final){
  do{
    if(inicio<final){
      inicio= inicio + 5;
    }else{
      inicio= inicio - 5;
    }
    mover(articulacion, inicio);
    delay(500); 
  }while(inicio!=final && inicio>0 && inicio<180 && final>0 && final<180);
}

void caida_munheca(){
  mover(HOMBRO, 20);
  delay(1000);
  mover(MUNHECA_IN, 170);
  delay(4000);
  mover(HOMBRO,50);
  delay(1000);
}

void agarrar_caja() {
  mover(BASE, 105);
  delay(1000);
  mover(HOMBRO, 20);
  delay(1000);
  mover(MUNHECA_IN, 170);
  delay(4000);
  suave(HOMBRO, 20, 80);
  mover(PINZA,  130);
  delay(1000);
  mover(HOMBRO, 70);
  delay(1000);
  suave(BASE, 105, 80);
  suave(HOMBRO, 70, 80);
  mover(PINZA, 70); 
  delay(1000);
  suave(HOMBRO, 80, 30); 
}

void subir() {

  //Agarrar Seccion Cámara
  mover(BASE, 80);
  suave(HOMBRO, 40, 80);
  mover(PINZA, 130);      
  delay(1000); 
  suave(HOMBRO, 80, 35);    
  suave(MUNHECA_IN, 170, 150);

  //Girar a la base superior
  suave(BASE, 80, 30);

  //Empieza rotación
  mover(HOMBRO, 40);
  delay(1000); 
  mover(PINZA, 70);
  delay(100);
  mover(HOMBRO, 35);
  delay(1000); 
  mover(MUNHECA_IN, 165);
  delay(1000);
  mover(PINZA, 130);
  delay(1000);
  mover(HOMBRO, 30);
  delay(1000); 
  mover(MUNHECA_IN,150);
  delay(1000); 
  mover(HOMBRO, 40);
  delay(1000);
  mover(PINZA, 70);
  delay(1000);
  mover(HOMBRO, 35);
  delay(1000); 
  mover(MUNHECA_IN, 165);
  delay(1000);
  mover(PINZA, 130);
  delay(1000);
  mover(HOMBRO, 30);
  delay(1000); 
  mover(MUNHECA_IN,150);
  delay(1000); 
  suave(HOMBRO, 30, 20);
  mover(MUNHECA_IN, 170);
  delay(4000);
  suave(BASE, 30, 80);
  mover(MUNHECA_ROT, 150);
  suave(HOMBRO, 20, 80);
  mover(PINZA, 70);
  delay(1000);
  suave(HOMBRO, 80, 30);
  mover(MUNHECA_ROT, 80);
  delay(1000);
    
}

void zona_vencido() {
  mover(BASE, 80);
  suave(HOMBRO,30 ,80);
  mover(PINZA, 130);
  delay(1500);
  suave(HOMBRO, 80, 30);
  suave(BASE, 80, 140);
  suave(HOMBRO, 30, 80);
  mover(PINZA, 70);
  delay(1500);
  suave(HOMBRO, 80, 30);
  delay(1500);
}

void zona_no_vencido() {
  mover(BASE, 80);
  suave(HOMBRO,30 ,80);
  mover(PINZA, 130);
  delay(1500);
  suave(HOMBRO, 80, 30);
  suave(BASE, 80, 125);
  suave(HOMBRO, 30, 80);
  mover(PINZA, 70);
  delay(1500);
  suave(HOMBRO, 80, 30);
  delay(1500);
}

void circuito1(){
  agarrar_caja();
  subir();
  zona_no_vencido();
}

void circuito2(){
  agarrar_caja();
  subir();
  zona_vencido();
}

//==========================================================
//==========================================================


void mover_servos_posicion(const int destino[6]) {
  for (int i = 0; i < 6; i++) {
    int actual = servos[i].read();
    if (actual == destino[i]) continue;

    int paso = (destino[i] > actual) ? 1 : -1;
    while (actual != destino[i]) {
      actual += paso;
      servos[i].write(actual);
    }
  }
}

void mover(Articulacion articulacion, int destino) {
  destino = constrain(destino, 0, 180);
  int actual = servos[articulacion].read();
  if (actual == destino) return;

  int paso = (destino > actual) ? 1 : -1;

  while (actual != destino) {
    actual += paso;
    servos[articulacion].write(actual);
  }
}

bool parsear_comando(const String& mensaje, String &nombre, int &angulo) {
  int espacio = mensaje.indexOf(' ');
  if (espacio == -1) return false;

  nombre = mensaje.substring(0, espacio);
  nombre.trim();
  nombre.toUpperCase();

  String angulo_str = mensaje.substring(espacio + 1);
  angulo_str.trim();
  angulo = angulo_str.toInt();
  angulo = constrain(angulo, 0, 180);

  return true;
}

bool nombre_a_articulacion(const String& nombre, Articulacion& resultado) {
  if (nombre == "BASE") resultado = BASE;
  else if (nombre == "HOMBRO") resultado = HOMBRO;
  else if (nombre == "CODO") resultado = CODO;
  else if (nombre == "MUNHECA_ROT") resultado = MUNHECA_ROT;
  else if (nombre == "MUNHECA_IN") resultado = MUNHECA_IN;
  else if (nombre == "PINZA") resultado = PINZA;
  else return false;
  return true;
}