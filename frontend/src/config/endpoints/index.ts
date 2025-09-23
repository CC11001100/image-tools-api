// API端点配置 - 模块化导出
export { basicEndpoints } from './basicEndpoints';
export { imageProcessingEndpoints } from './imageProcessingEndpoints';
export { geometryEndpoints } from './geometryEndpoints';
export { advancedEndpoints } from './advancedEndpoints';

// 原有的单独端点导出（保持向后兼容）
export * from './annotationEndpoint';
export * from './blendEndpoint';
export * from './canvasEndpoint';
export * from './colorEndpoint';
export * from './cropEndpoint';
export * from './enhanceEndpoint';
export * from './filterEndpoint';
export * from './formatEndpoint';
export * from './gifEndpoint';
export * from './maskEndpoint';
export * from './overlayEndpoint';
export * from './perspectiveEndpoint';
export * from './pixelateEndpoint';
export * from './resizeEndpoint';
export * from './stitchEndpoint';
export * from './transformEndpoint';
export * from './watermarkEndpoint';
export * from './advancedTextEndpoint';