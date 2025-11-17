import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

import Layout from './components/Layout';
import { SearchProvider } from './contexts/SearchContext';
import { AuthProvider } from './contexts/AuthContext';
import Home from './pages/Home';
import WatermarkPage from './pages/WatermarkPage';
import ResizePage from './pages/ResizePage';
import FilterPage from './pages/FilterPage';
import ArtFilterPage from './pages/ArtFilterPage';
import CropPage from './pages/CropPage';
import TransformPage from './pages/TransformPage';
import PerspectivePage from './pages/PerspectivePage';
import BlendPage from './pages/BlendPage';
import StitchPage from './pages/StitchPage';
import FormatPage from './pages/FormatPage';
import NoisePage from './pages/NoisePage';
import ColorPage from './pages/ColorPage';
import EnhancePage from './pages/EnhancePage';
import PixelatePage from './pages/PixelatePage';
import CanvasPage from './pages/CanvasPage';
import TextPage from './pages/AdvancedTextPage';
import OverlayPage from './pages/OverlayPage';
import MaskPage from './pages/MaskPage';

import GifPage from './pages/GifPage';
import ImageToGifPage from './pages/ImageToGifPage';
import GifExtractPage from './pages/GifExtractPage';
import AnnotationPage from './pages/AnnotationPage';
import ApiDocs from './pages/ApiDocs';
import AuthTestPage from './pages/AuthTestPage';

// 创建一个自定义主题
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <SearchProvider>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/watermark" element={<WatermarkPage />} />
              <Route path="/resize" element={<ResizePage />} />
              <Route path="/crop" element={<CropPage />} />
              <Route path="/transform" element={<TransformPage />} />
              <Route path="/perspective" element={<PerspectivePage />} />
              <Route path="/canvas" element={<CanvasPage />} />
              <Route path="/filter" element={<FilterPage />} />
              <Route path="/art-filter" element={<ArtFilterPage />} />
              <Route path="/color" element={<ColorPage />} />
              <Route path="/enhance" element={<EnhancePage />} />
              <Route path="/noise" element={<NoisePage />} />
              <Route path="/pixelate" element={<PixelatePage />} />
              <Route path="/blend" element={<BlendPage />} />
              <Route path="/stitch" element={<StitchPage />} />
              <Route path="/overlay" element={<OverlayPage />} />
              <Route path="/mask" element={<MaskPage />} />
              <Route path="/format" element={<FormatPage />} />
              <Route path="/text" element={<TextPage />} />
              <Route path="/annotation" element={<AnnotationPage />} />

              <Route path="/gif-extract" element={<GifExtractPage />} />
              <Route path="/gif-create" element={<ImageToGifPage />} />
              <Route path="/gif-optimize" element={<GifPage />} />
              <Route path="/api-docs" element={<ApiDocs />} />
              <Route path="/auth-test" element={<AuthTestPage />} />
            </Routes>
          </Layout>
        </SearchProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App; 