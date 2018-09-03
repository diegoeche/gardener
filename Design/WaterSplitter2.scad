// import("/Users/wooga/Downloads/Motorized_Door_Lock/files/Gear.STL");

module rack () {
  translate([-90,-22,0]) {
    intersection() {
      import("/Users/wooga/Downloads/Gear_Rack2.stl");
      // cube(200, 200, 200);    
    }  
  }
}
holes=5;
layer_h= 4;
radius = 30;
space=30; // degrees
distance= 22;
valve_r = 3.5;
border = 3;
offset = 1.0;


module pipe() {
  difference() {
    cylinder(r=valve_r + 0.5, h=layer_h * 2.5);
    cylinder(r=valve_r - 1, h=100);
    // translate([0,0,9]) sphere(r=valve_r * 1.3);  
  }    
}

module top () {
  union() {
    rack();
    translate([90, 7.5, 7]) pipe();    
  }  
}

module realTop() {
    difference() {
      top();
      //translate([90, 7.5, -10]) cylinder(r=valve_r - 1, h=100);    
    }
}

module bottom() {
 difference() {
   cube([80, 20, 10]);
   translate([-21, 2.5, 4]) %top();   
 }
}
top();
// bottom();

// realTop();