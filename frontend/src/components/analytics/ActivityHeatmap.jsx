import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Tooltip,
  useTheme
} from '@mui/material';
import { format, parseISO, eachDayOfInterval, subDays } from 'date-fns';

const CELL_SIZE = 10;
const CELL_PADDING = 2;
const DAYS_IN_WEEK = 7;
const WEEKS_TO_SHOW = 52;

const ActivityHeatmap = ({ data }) => {
  const theme = useTheme();

  // Generate dates for the last year
  const endDate = new Date();
  const startDate = subDays(endDate, 365);
  const dates = eachDayOfInterval({ start: startDate, end: endDate });

  // Calculate max activity value for color scaling
  const maxActivity = Math.max(...Object.values(data));

  const getColor = (value) => {
    if (!value) return theme.palette.action.hover;
    
    const intensity = value / maxActivity;
    return theme.palette.primary.main + Math.round(intensity * 80).toString(16).padStart(2, '0');
  };

  const formatTooltipDate = (date) => {
    return format(date, 'MMM d, yyyy');
  };

  const formatActivityValue = (value) => {
    if (!value) return 'No activity';
    const hours = Math.floor(value / 60);
    const minutes = value % 60;
    return `${hours}h ${minutes}m of study`;
  };

  // Group dates by week
  const weeks = [];
  let currentWeek = [];
  
  dates.forEach((date) => {
    currentWeek.push(date);
    if (currentWeek.length === DAYS_IN_WEEK) {
      weeks.push(currentWeek);
      currentWeek = [];
    }
  });

  if (currentWeek.length > 0) {
    weeks.push(currentWeek);
  }

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Activity Heatmap
      </Typography>
      
      <Box sx={{ display: 'flex', alignItems: 'flex-start', mt: 2 }}>
        {/* Days of week labels */}
        <Box sx={{ mr: 2, mt: CELL_SIZE + CELL_PADDING }}>
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
            <Typography
              key={day}
              variant="caption"
              sx={{
                display: 'block',
                height: CELL_SIZE + CELL_PADDING,
                lineHeight: `${CELL_SIZE}px`,
                textAlign: 'right',
                pr: 1
              }}
            >
              {day}
            </Typography>
          ))}
        </Box>

        {/* Heatmap grid */}
        <Box sx={{ display: 'flex' }}>
          {weeks.map((week, weekIndex) => (
            <Box key={weekIndex} sx={{ display: 'flex', flexDirection: 'column' }}>
              {week.map((date, dayIndex) => {
                const dateKey = format(date, 'yyyy-MM-dd');
                const value = data[dateKey] || 0;

                return (
                  <Tooltip
                    key={dayIndex}
                    title={`${formatTooltipDate(date)}: ${formatActivityValue(value)}`}
                    arrow
                  >
                    <Box
                      sx={{
                        width: CELL_SIZE,
                        height: CELL_SIZE,
                        m: `${CELL_PADDING/2}px`,
                        bgcolor: getColor(value),
                        borderRadius: 0.5,
                        cursor: 'pointer',
                        '&:hover': {
                          opacity: 0.8
                        }
                      }}
                    />
                  </Tooltip>
                );
              })}
            </Box>
          ))}
        </Box>
      </Box>

      {/* Legend */}
      <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
        <Typography variant="caption" sx={{ mr: 1 }}>
          Less
        </Typography>
        {[0, 0.25, 0.5, 0.75, 1].map((intensity, i) => (
          <Box
            key={i}
            sx={{
              width: CELL_SIZE,
              height: CELL_SIZE,
              mx: 0.5,
              bgcolor: getColor(intensity * maxActivity),
              borderRadius: 0.5
            }}
          />
        ))}
        <Typography variant="caption" sx={{ ml: 1 }}>
          More
        </Typography>
      </Box>
    </Paper>
  );
};

export default ActivityHeatmap;
