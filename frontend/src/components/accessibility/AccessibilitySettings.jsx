import React from 'react';
import {
  Box,
  Typography,
  Switch,
  FormControl,
  FormControlLabel,
  Select,
  MenuItem,
  Paper,
  Stack,
  Divider,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Contrast as ContrastIcon,
  TextFields as TextFieldsIcon,
  Speed as SpeedIcon,
  VolumeUp as VolumeUpIcon,
  FormatLineSpacing as LineSpacingIcon,
  Language as LanguageIcon
} from '@mui/icons-material';
import { useAccessibility } from './AccessibilityProvider';

const AccessibilitySettings = () => {
  const {
    settings,
    setFontSize,
    setContrast,
    toggleReducedMotion,
    toggleScreenReader,
    toggleDyslexicFont,
    setLineSpacing,
    setLanguage
  } = useAccessibility();

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Accessibility Settings
      </Typography>

      <Stack spacing={3}>
        {/* Font Size */}
        <Box>
          <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <TextFieldsIcon sx={{ mr: 1 }} /> Text Size
          </Typography>
          <FormControl fullWidth>
            <Select
              value={settings.fontSize}
              onChange={(e) => setFontSize(e.target.value)}
              size="small"
            >
              <MenuItem value="small">Small</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="large">Large</MenuItem>
              <MenuItem value="x-large">Extra Large</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Divider />

        {/* Contrast */}
        <Box>
          <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <ContrastIcon sx={{ mr: 1 }} /> Contrast
          </Typography>
          <FormControl fullWidth>
            <Select
              value={settings.contrast}
              onChange={(e) => setContrast(e.target.value)}
              size="small"
            >
              <MenuItem value="normal">Normal Contrast</MenuItem>
              <MenuItem value="high">High Contrast</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Divider />

        {/* Line Spacing */}
        <Box>
          <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <LineSpacingIcon sx={{ mr: 1 }} /> Line Spacing
          </Typography>
          <FormControl fullWidth>
            <Select
              value={settings.lineSpacing}
              onChange={(e) => setLineSpacing(e.target.value)}
              size="small"
            >
              <MenuItem value="tight">Tight</MenuItem>
              <MenuItem value="normal">Normal</MenuItem>
              <MenuItem value="loose">Loose</MenuItem>
              <MenuItem value="very-loose">Very Loose</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Divider />

        {/* Language */}
        <Box>
          <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <LanguageIcon sx={{ mr: 1 }} /> Language
          </Typography>
          <FormControl fullWidth>
            <Select
              value={settings.language}
              onChange={(e) => setLanguage(e.target.value)}
              size="small"
            >
              <MenuItem value="en">English</MenuItem>
              <MenuItem value="ro">Romanian</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Divider />

        {/* Toggles */}
        <Stack spacing={2}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.reducedMotion}
                onChange={toggleReducedMotion}
              />
            }
            label={
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <SpeedIcon sx={{ mr: 1 }} />
                Reduced Motion
              </Box>
            }
          />

          <FormControlLabel
            control={
              <Switch
                checked={settings.screenReader}
                onChange={toggleScreenReader}
              />
            }
            label={
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <VolumeUpIcon sx={{ mr: 1 }} />
                Screen Reader Support
              </Box>
            }
          />

          <FormControlLabel
            control={
              <Switch
                checked={settings.dyslexicFont}
                onChange={toggleDyslexicFont}
              />
            }
            label={
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TextFieldsIcon sx={{ mr: 1 }} />
                Dyslexic-Friendly Font
              </Box>
            }
          />
        </Stack>
      </Stack>
    </Paper>
  );
};

export default AccessibilitySettings;
