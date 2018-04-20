holes=5;
layer_h= 4;
radius = 30;
space=30; // degrees
distance= 22;
valve_r = 3.5;
border = 3;
offset = 1.0;
module arm(x, y, z, d) {
CubePoints = [
  [  0,  0,  0 ],  //0
  [ x,  0,  0 ],  //1
  [ x-d,  y,  0 ],  //2
  [ 0+d, y,  0 ],  //3
  [ 0,  0,  z ],  //4
  [ x,  0,  z ],  //5
  [ x-d,  y,  z ],  //6
  [ 0+d,  y,  z ]]; //7
  
CubeFaces = [
  [0,1,2,3],  // bottom
  [4,5,1,0],  // front
  [7,6,5,4],  // top
  [5,6,2,1],  // right
  [6,7,3,2],  // back
  [7,4,0,3]]; // left
  
 polyhedron( CubePoints, CubeFaces );    
 translate([0,0,z]) rotate([180,0,0]) polyhedron( CubePoints, CubeFaces );
 translate([x/2,y,0]) cylinder(h=z, r=(x/2)-d);
 translate([x/2,-y,0]) cylinder(h=z, r=(x/2)-d);
 translate([x/2,0,0]) cylinder(h=z*2.5, r=(x/2) * 1.2);
}
module servo() {
  import("/Users/wooga/Downloads/microServo-sg90.stl");    
};
// $fn = 50;

union() {    
    difference() {
        union() {
            cylinder(r=radius, h=layer_h*0.7);
            layers = 10;
            h = 0.2;
            for(i=[0:layers]){
              translate([0,0,layer_h * 0.7 + i * h]) cylinder(r=radius + (i*h), h);
             }
            
            translate([0,0,-layer_h - 1]) difference() {
                cylinder(r=radius + offset + border, h=layer_h * 2);
                translate([0,0,-0.1]) cylinder(r=radius + offset, h=(layer_h * 2) + 0.2);
            }
            for(i=[0:holes]) {        
                translate([distance * sin(i * space),
                           distance * cos(i * space), 
                           layer_h]) {
                  cylinder(r=valve_r + 0.5, h=layer_h * 2.5);
                }    
            }    
        }
        for(i=[0:holes]) {        
            translate([distance * sin(i * space),
                       distance * cos(i * space), 
                       -10]) {
              cylinder(r=valve_r - 1, h=100);
              translate([0,0,9]) sphere(r=valve_r * 1.2);
            }    
        }
        translate([0,0,-1]) cylinder(r=2.3, h=100);
        rotate([0,180,0]){
          translate([-3,0, -layer_h - 1.1]) arm(6, 15, 2.2, 1);
          
        }
    }
}

translate([0,0, (-2 * layer_h - 0)]) difference() {
  union() {
    difference() {
      cylinder(r=radius, h=layer_h * 2);
      translate([radius/3, -radius, -0.1]) cube([radius * 2, radius * 2, layer_h * 2 + 1]);
      rotate([0,180,0]) translate([radius/3, -radius, -layer_h * 2 - 0.1]) cube([radius * 2, radius * 2, layer_h * 2 + 1]);
    }
    translate([0, -distance, -8]) cylinder(r=valve_r, h=layer_h * 2);
    translate([-radius/3, radius - border,0]) cube([(2 * radius/3),radius * 0.9, layer_h - offset]);
  }
  translate([0, -(distance * cos(0)), -10]) cylinder(r=valve_r - 1.5, h=layer_h * 5);
  scale(1.05) rotate([0,0,90]) translate([-6,-6,-18.5]) servo();
  translate([0, 20, -20]) cylinder(r=1.2, h=100);
  translate([0, -9, -20]) cylinder(r=1.2, h=100);
}
