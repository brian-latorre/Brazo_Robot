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
// completa. Sirve para pruebas. Mensaje no necesariamente tiene el mismo nombre que la función a la que llama
String mensaje;

// Arreglo de 6 servos, uno para cada articulación
Servo servos[6];    // servos[BASE], servos[HOMBRO] , servos[CODO] , servos[MUNHECA_ROT], servos[MUNHECA_IN], servos[PINZA]

// Posición inicial donde el brazo está seguro sin golpear nada. 
const int home[6] = {
  105,  // BASE
   20,  // HOMBRO
   5,  // CODO
   80,  // MUNHECA_ROT
  170,  // MUNHECA_IN
   70   // PINZA
};

// Posiciones alternativas
const int posicion_1[6] = {80, 70, 7, 80, 160, 0};

void mover_servos_posicion(const int destino[6]);
void mover(Articulacion articulacion, int destino);
bool parsear_comando(const String& mensaje, String &nombre, int &angulo);
bool nombre_a_articulacion(const String& nombre, Articulacion& resultado);
void agarrar_caja();
void zona_vencido();
void zona_no_vencido();
void suave(Articulacion articulacion, int inicio, int final);
void suave_2(Articulacion articulacion, int inicio, int final);
void circuito1();
void circuito2();
void HOME();
void arriba_abajo();
void rotar();
void rotacion_1();
void rotacion_2();
void rotacion_3();
void rotacion_4();

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
    mensaje = Serial.readStringUntil('\n');
    mensaje.trim(); 

    String nombre;
    int angulo;

    if (parsear_comando(mensaje, nombre, angulo)) {
      Articulacion articulacion;
      if (nombre_a_articulacion(nombre, articulacion)) {
        mover(articulacion, angulo);
        Serial.println("OK");
      } else {
        Serial.println("ERROR: Articulación no válida");
      }
      return;
    }

    // --- Mensajes de posición predeterminada ---
    // Si deseas agregar un mensaje para que haga un movimiento el brazo, agregalo aqui
    if (mensaje == "POS1") mover_servos_posicion(posicion_1);
    else if (mensaje == "CAJA") agarrar_caja();
    else if (mensaje == "VENCIDO") zona_vencido();
    else if (mensaje == "NO_VENCIDO") zona_no_vencido();
    else if(mensaje == "SUBIR") subir();
    else if(mensaje == "CIRCUITO1") circuito1();
    else if(mensaje == "CIRCUITO2") circuito2();
    else if(mensaje=="HOME") HOME();
    else if(mensaje=="ROTACION_1") rotacion_1();
    else if(mensaje=="ROTACION_2") rotacion_2();
    else if(mensaje=="ROTACION_3") rotacion_3();
    else if(mensaje=="ROTACION_4") rotacion_4();
    else {
      Serial.println("ERROR: Mensaje no reconocido");
      return;
    }

    Serial.println("OK");
  }
}

//==========codigo Brazo-Robot final=============
//===============================================

void HOME(){
  mover(BASE, 105);
  mover(HOMBRO, 20);
  mover(CODO, 5);
  mover(MUNHECA_IN, 170);
  mover(MUNHECA_ROT, 80);
  mover(PINZA, 70);
}

void suave(Articulacion articulacion, int inicio, int final){
  do{
    if(inicio<final){
      inicio= inicio + 1;
    }else{
      inicio= inicio - 1;
    }
    mover(articulacion, inicio);
    delay(40); 
  }while(inicio!=final && inicio>0 && inicio<180 && final>0 && final<180);
}

void suave_2(Articulacion articulacion, int inicio, int final){
  do{
    if(inicio<final){
      inicio= inicio + 5;
    }else{
      inicio= inicio - 5;
    }
    mover(articulacion, inicio);
    delay(40); 
  }while(inicio!=final && inicio>0 && inicio<180 && final>0 && final<180);
}

void agarrar_caja() {
  suave(HOMBRO, 20, 80);
  suave(PINZA, 70, 130);
  delay(750);
  mover(HOMBRO, 75);
  delay(750);
  suave(BASE, 105, 80);
  suave(HOMBRO, 75, 80);
  suave(PINZA, 130, 70);
  delay(750);
  mover(HOMBRO, 60);
}

void rotacion_1() {
  mover(MUNHECA_ROT, 10);
  mover(BASE, 81);
  suave(HOMBRO, 60, 75);
  delay(750);
  suave(PINZA, 70, 130);
  delay(750);
  mover(HOMBRO, 73);
  delay(750);
  mover(MUNHECA_ROT, 80);
  mover(BASE, 79);
  suave(HOMBRO, 73, 75);
  suave(PINZA, 130, 70);
  delay(750);
  mover(HOMBRO, 60);
}

void rotacion_2() {
  mover(MUNHECA_ROT, 10);
  mover(BASE, 81);
  suave(HOMBRO, 60, 75);
  delay(750);
  suave(PINZA, 70, 130);
  delay(750);
  mover(HOMBRO, 73);
  delay(750);
  mover(MUNHECA_ROT, 80);
  mover(BASE, 79);
  suave(HOMBRO, 73, 75);
  suave(PINZA, 130, 70);
  delay(750);
  mover(HOMBRO, 60);
}

void rotacion_3() {
  mover(MUNHECA_ROT, 10);
  mover(BASE, 81);
  suave(HOMBRO, 60, 75);
  delay(750);
  suave(PINZA, 70, 130);
  delay(750);
  mover(HOMBRO, 73);
  delay(750);
  mover(MUNHECA_ROT, 80);
  mover(BASE, 79);
  suave(HOMBRO, 73, 75);
  suave(PINZA, 130, 70);
  delay(750);
  mover(HOMBRO, 60);
}

void rotacion_4() {
  mover(MUNHECA_ROT, 10);
  mover(BASE, 80);
  suave(HOMBRO, 60, 75);
  delay(750);
  suave(PINZA, 70, 130);
  delay(750);
  suave_2(HOMBRO, 75, 25);
  delay(300);
  mover(MUNHECA_ROT, 80);
  mover(MUNHECA_IN, 160);
  suave(BASE, 81, 28);
  suave(HOMBRO, 25, 30);
  delay(500);
  suave(PINZA, 130, 90);
  delay(300);
  mover(MUNHECA_IN, 170);
  suave(PINZA, 90, 70);
  delay(500);
  suave(PINZA, 70, 130);
  delay(500);
  mover(HOMBRO, 25);
  delay(150);
  suave(BASE, 28, 81);
  suave(HOMBRO, 25, 75);
  suave(PINZA, 130, 70);
  delay(750);
  mover(HOMBRO, 60);
}

void subir() {

  //Agarrar Seccion Cámara
  mover(BASE, 80);
  suave(HOMBRO, 40, 80);
  mover(PINZA, 130);      
  delay(1000); 
  suave(HOMBRO, 80, 35);    
  suave(MUNHECA_IN, 170, 150);
  suave(HOMBRO, 35, 40);

  //Girar a la base superior
  suave(BASE, 80, 30);
  /////////////////////////

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

void rotar(){
  mover(MUNHECA_ROT, 150);
}

void arriba_abajo() {

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
  suave(HOMBRO, 20, 80);
  mover(PINZA, 70);
  delay(1000);
  suave(HOMBRO, 80, 30);
  mover(MUNHECA_ROT, 80);
  delay(1000);
}

void zona_vencido() {
  suave(HOMBRO,60 ,75);
  delay(750);
  suave(PINZA, 70, 160);
  delay(750);
  mover(HOMBRO, 72);
  delay(750);
  mover(BASE, 86);
  suave(BASE, 86, 140);
  suave(HOMBRO, 73, 75);
  mover(PINZA, 70);
  delay(500);
  suave(HOMBRO, 80, 30);
}

void zona_no_vencido() {
  suave(HOMBRO,60 ,75);
  delay(750);
  suave(PINZA, 70, 160);
  delay(750);
  mover(HOMBRO, 72);
  delay(750);
  mover(BASE, 86);
  suave(BASE, 86, 125);
  suave(HOMBRO, 73, 75);
  mover(PINZA, 70);
  delay(500);
  suave(HOMBRO, 80, 30);
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
      delay(100);
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
  if(espacio == -1) return false;

  nombre= mensaje.substring(0, espacio);
  nombre.trim();
  nombre.toUpperCase();

  String angulo_str=mensaje.substring(espacio + 1);
  angulo_str.trim();
  angulo= angulo_str.toInt();
  angulo= constrain(angulo, 0, 180);
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
