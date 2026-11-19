import { Color, FrontSide, ShaderMaterial } from 'three'

// World-space washes stay attached to the buildings while the camera moves.
// Pencil contours are added as geometry; lettering uses a separate unlit material.
export function watercolourMaterial(color: Color) {
  return new ShaderMaterial({
    side: FrontSide,
    uniforms: { pigment: { value: color }, mist: { value: new Color('#d7e0df') } },
    vertexShader: `
      varying vec3 worldPoint;
      varying vec3 faceNormal;
      varying float viewDepth;
      void main() {
        vec4 world = modelMatrix * vec4(position, 1.0);
        worldPoint = world.xyz;
        faceNormal = normalize(mat3(modelMatrix) * normal);
        vec4 view = viewMatrix * world;
        viewDepth = -view.z;
        gl_Position = projectionMatrix * view;
      }
    `,
    fragmentShader: `
      uniform vec3 pigment;
      uniform vec3 mist;
      varying vec3 worldPoint;
      varying vec3 faceNormal;
      varying float viewDepth;
      float hash(vec3 p) { return fract(sin(dot(p, vec3(127.1,311.7,74.7))) * 43758.5453); }
      float noise(vec3 p) {
        vec3 i=floor(p), f=fract(p); f=f*f*(3.0-2.0*f);
        return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
          mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z);
      }
      void main() {
        vec3 normal=normalize(faceNormal);
        float light=dot(normal,normalize(vec3(-.48,.72,.55)));
        float wash=noise(worldPoint*1.9)*.65+noise(worldPoint*5.7)*.35;
        float shade=smoothstep(.03,.42,light+wash*.12);
        vec3 colour=pigment*mix(vec3(.76,.79,.87),vec3(1.0),shade);
        // Pigment granulation and slight pooling at a wash boundary.
        colour*=.95+wash*.1;
        colour*=1.0-(1.0-smoothstep(.0,.13,abs(light-.2)))*.035;
        // Warm light stays inside the warehouse room; two broad lamps above the
        // bar and seating softly colour the plaster, timber and concrete.
        float room=step(-4.4,worldPoint.x)*step(worldPoint.x,4.4)*step(-18.3,worldPoint.z)*step(worldPoint.z,-13.0)*step(worldPoint.y,3.95);
        float barLight=1.0/(1.0+dot(worldPoint-vec3(-1.6,2.75,-16.6),worldPoint-vec3(-1.6,2.75,-16.6))*.35);
        float seatLight=1.0/(1.0+dot(worldPoint-vec3(2.3,2.75,-15.8),worldPoint-vec3(2.3,2.75,-15.8))*.5);
        colour=mix(colour,colour*mix(vec3(.88,.83,.75),vec3(1.22,1.1,.88),min(1.0,barLight+seatLight)),room*.7);
        float grain=hash(vec3(gl_FragCoord.xy,17.0));
        colour+=(grain-.5)*.012;
        colour=mix(colour,mist,smoothstep(32.0,110.0,viewDepth)*.8);
        gl_FragColor=vec4(colour,1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }
    `,
  })
}
