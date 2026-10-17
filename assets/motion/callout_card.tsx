import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface CalloutCardProps {
  title: string;
  badge?: string;
  accentColor?: string;
  styleMode?: 'dark_glass' | 'monochrome' | 'documentary';
}


export const CalloutCard: React.FC<CalloutCardProps> = ({
  title,
  badge = 'ФАКТ',
  accentColor = '#FFD93D',
  styleMode = 'dark_glass',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({
    frame,
    fps,
    config: {
      damping: 14,
      mass: 0.6,
      stiffness: 160,
    },
  });

  const scale = interpolate(pop, [0, 1], [0.85, 1]);
  const opacity = interpolate(frame, [0, 5], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <div
      style={{
        transform: `scale(${scale})`,
        opacity,
        display: 'inline-flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        gap: 8,
        padding: '18px 24px',
        borderRadius: 14,
        background: 'rgba(20, 20, 22, 0.88)',
        backdropFilter: 'blur(16px)',
        border: '1px solid rgba(255, 255, 255, 0.14)',
        boxShadow: '0 12px 28px -6px rgba(0, 0, 0, 0.5)',
        maxWidth: 780,
      }}
    >
      {badge && (
        <span
          style={{
            fontSize: 13,
            fontWeight: 800,
            letterSpacing: 1.2,
            textTransform: 'uppercase',
            color: accentColor,
            background: 'rgba(255, 255, 255, 0.06)',
            padding: '4px 10px',
            borderRadius: 6,
          }}
        >
          {badge}
        </span>
      )}
      <div
        style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: 28,
          fontWeight: 700,
          color: '#FFFFFF',
          lineHeight: 1.25,
        }}
      >
        {title}
      </div>
    </div>
  );
};
