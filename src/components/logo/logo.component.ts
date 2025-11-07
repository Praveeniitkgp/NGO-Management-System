
import { Component, ElementRef, viewChild, AfterViewInit, OnDestroy, ChangeDetectionStrategy, effect, signal } from '@angular/core';
import * as THREE from 'three';

@Component({
  selector: 'app-3d-logo',
  template: '<div #canvasContainer class="w-full h-full"></div>',
  imports: [],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LogoComponent implements AfterViewInit, OnDestroy {
  canvasContainer = viewChild.required<ElementRef<HTMLDivElement>>('canvasContainer');

  private renderer!: THREE.WebGLRenderer;
  private scene!: THREE.Scene;
  private camera!: THREE.PerspectiveCamera;
  private mesh!: THREE.Mesh;
  private animationFrameId: number | null = null;
  
  private dimensions = signal({ width: 0, height: 0 });

  constructor() {
    effect(() => {
        const { width, height } = this.dimensions();
        if (width > 0 && height > 0) {
            this.resizeRenderer(width, height);
        }
    });
  }

  ngAfterViewInit(): void {
    this.initThree();
    this.setDimensions();
    this.animate();
  }

  ngOnDestroy(): void {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    this.renderer.dispose();
  }
  
  setDimensions() {
    const container = this.canvasContainer().nativeElement;
    this.dimensions.set({ width: container.clientWidth, height: container.clientHeight });
  }

  private initThree(): void {
    const container = this.canvasContainer().nativeElement;
    const { width, height } = container.getBoundingClientRect();

    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    this.camera.position.z = 5;

    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(this.renderer.domElement);

    const geometry = new THREE.TorusKnotGeometry(1.5, 0.4, 100, 16);
    const material = new THREE.MeshStandardMaterial({
      color: 0x3b82f6, // blue-500
      metalness: 0.7,
      roughness: 0.3,
    });
    this.mesh = new THREE.Mesh(geometry, material);
    this.scene.add(this.mesh);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 1.5);
    pointLight.position.set(5, 5, 5);
    this.scene.add(pointLight);
  }

  private resizeRenderer(width: number, height: number): void {
      if (this.renderer && this.camera) {
          this.camera.aspect = width / height;
          this.camera.updateProjectionMatrix();
          this.renderer.setSize(width, height);
      }
  }

  private animate = (): void => {
    this.animationFrameId = requestAnimationFrame(this.animate);

    if (this.mesh) {
      this.mesh.rotation.x += 0.003;
      this.mesh.rotation.y += 0.003;
    }

    this.renderer.render(this.scene, this.camera);
  }
}
