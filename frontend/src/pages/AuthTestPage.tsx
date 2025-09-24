/**
 * AuthTestPage - 认证测试页面
 */

import React from 'react';
import QuickAuthTest from '../components/QuickAuthTest';

const AuthTestPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">认证测试</h1>
      <QuickAuthTest />
    </div>
  );
};

export default AuthTestPage;
