import React, { createContext, useContext, useState, useEffect } from 'react';

const AccessibilityContext = createContext();

export const useAccessibility = () => {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within an AccessibilityProvider');
  }
  return context;
};

export const AccessibilityProvider = ({ children }) => {
  const [settings, setSettings] = useState(() => {
    const saved = localStorage.getItem('accessibility_settings');
    return saved ? JSON.parse(saved) : {
      fontSize: 'medium',
      contrast: 'normal',
      reducedMotion: false,
      screenReader: false,
      dyslexicFont: false,
      lineSpacing: 'normal',
      language: 'en'
    };
  });

  useEffect(() => {
    localStorage.setItem('accessibility_settings', JSON.stringify(settings));
    applyAccessibilityStyles(settings);
  }, [settings]);

  const updateSettings = (newSettings) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  const applyAccessibilityStyles = (settings) => {
    const root = document.documentElement;
    
    // Font size
    const fontSizes = {
      small: '0.875rem',
      medium: '1rem',
      large: '1.125rem',
      'x-large': '1.25rem'
    };
    root.style.setProperty('--base-font-size', fontSizes[settings.fontSize]);

    // Contrast
    if (settings.contrast === 'high') {
      document.body.classList.add('high-contrast');
    } else {
      document.body.classList.remove('high-contrast');
    }

    // Reduced motion
    if (settings.reducedMotion) {
      root.style.setProperty('--transition-duration', '0s');
    } else {
      root.style.setProperty('--transition-duration', '0.3s');
    }

    // Dyslexic font
    if (settings.dyslexicFont) {
      root.style.setProperty('--font-family', '"OpenDyslexic", sans-serif');
    } else {
      root.style.setProperty('--font-family', 'Roboto, sans-serif');
    }

    // Line spacing
    const lineSpacings = {
      tight: '1.4',
      normal: '1.6',
      loose: '1.8',
      'very-loose': '2'
    };
    root.style.setProperty('--line-height', lineSpacings[settings.lineSpacing]);
  };

  const value = {
    settings,
    updateSettings,
    toggleScreenReader: () => {
      updateSettings({ screenReader: !settings.screenReader });
    },
    toggleDyslexicFont: () => {
      updateSettings({ dyslexicFont: !settings.dyslexicFont });
    },
    setFontSize: (size) => {
      updateSettings({ fontSize: size });
    },
    setContrast: (contrast) => {
      updateSettings({ contrast });
    },
    setLineSpacing: (spacing) => {
      updateSettings({ lineSpacing: spacing });
    },
    setLanguage: (language) => {
      updateSettings({ language });
    },
    toggleReducedMotion: () => {
      updateSettings({ reducedMotion: !settings.reducedMotion });
    }
  };

  return (
    <AccessibilityContext.Provider value={value}>
      {children}
    </AccessibilityContext.Provider>
  );
};
