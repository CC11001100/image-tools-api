export interface BlendExample {
  title: string;
  description: string;
  baseImages: string[];
  overlayImages: string[];
  resultImages: string[];
  apiParams: Record<string, any>;
}

export interface BlendShowcaseProps {
  title: string;
  description: string;
  examples: BlendExample[];
  onApplyParams?: (params: Record<string, any>) => void;
}

export interface GalleryImage {
  src: string;
  alt: string;
  title?: string;
  description?: string;
}
