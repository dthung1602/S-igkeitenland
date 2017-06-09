PImage img;

void setup () {
  img = loadImage("./coke.png");
}

void draw() {
  String s [] = new String [0];
  img.loadPixels();
  
  int red = color(255, 0, 0);
  int black = color(0, 0, 0);
  int white = color(255, 255, 255);
  
  for (int y = img.height - 1; y >= 0; y--) {
    int r = 0;
    char c = 's';
    for (int x = 0; x < img.width; x++) {
      int loc = x + y*img.width;
      
      if (img.pixels[loc] == 0) {
        print(" ");
        continue;
      }
      
      if (img.pixels[loc] == red) 
        c = 'R';
      else if (img.pixels[loc] == black) 
        c = 'B';
      else 
        c = 'W';
      print(c);
      r++;   
    }
    println("  | ", r);
    s = (String []) append(s, str(r/2) + " " + str(c));
    
  }
  
  saveStrings("coke_tower.txt", s);
  exit();
}