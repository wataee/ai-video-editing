import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface DeviceMockupProps {
  imageSrc?: string;
  videoSrc?: string;
  type?: 'phone' | 'browser';
  title?: string;
}

/**
 * DeviceMockup — Минималистичный премиальный мокап смартфона / браузера.
 * Без перегруженных градиентов, со стильной темной рамкой и spring-анимацией.
 */
export const DeviceMockup: React.FC<DeviceMockupProps> = ({
  imageSrc,
  type = 'phone',
  title = 'Proof / Reference',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: {
      damping: 16,
      mass: 0.7,
      stiffness: 140,
    },
  });

  const scale = interpolate(entrance, [0, 1], [0.88, 1]);
  const translateY = interpolate(entrance, [0, 1], [80, 0]);
  const opacity = interpolate(entrance, [0, 0.3], [0, 1], { extrapolateRight: 'clamp' });

  if (type === 'phone') {
    return (
      <div
        style={{
          width: 380,
          height: 760,
          borderRadius: 44,
          backgroundColor: '#18181B',
          border: '4px solid #27272A',
          boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.7)',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          transform: `translateY(${translateY}px) scale(${scale})`,
          opacity,
          position: 'relative',
        }}
      >
        {/* Dynamic Island / Notch */}
        <div
          style={{
            position: 'absolute',
            top: 14,
            left: '50%',
            transform: 'translateX(-50%)',
            width: 110,
            height: 26,
            borderRadius: 20,
            backgroundColor: '#000000',
            zIndex: 20,
          }}
        />

        {/* Экран устройства */}
        <div
          style={{
            width: '100%',
            height: '100%',
            backgroundColor: '#09090B',
            overflow: 'hidden',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          {imageSrc && (
            <img
              src={imageSrc}
              alt={title}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
              }}
            />
          )}
        </div>
      </div>
    );
  }

  // Browser Mockup
  return (
    <div
      style={{
        width: '90%',
        maxWidth: 720,
        borderRadius: 16,
        backgroundColor: '#18181B',
        border: '1px solid #27272A',
        boxShadow: '0 20px 50px rgba(0, 0, 0, 0.6)',
        overflow: 'hidden',
        transform: `translateY(${translateY}px) scale(${scale})`,
        opacity,
      }}
    >
      {/* Header bar with dots */}
      <div
        style={{
          height: 40,
          backgroundColor: '#202024',
          display: 'flex',
          alignItems: 'center',
          padding: '0 16px',
          gap: 8,
          borderBottom: '1px solid #27272A',
        }}
      >
        <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#EF4444' }} />
        <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#F59E0B' }} />
        <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#10B981' }} />
        <div
          style={{
            marginLeft: 16,
            fontSize: 12,
            fontFamily: 'Inter, sans-serif',
            color: '#71717A',
          }}
        >
          {title}
        </div>
      </div>
      {/* Content Area */}
      <div style={{ padding: 12, backgroundColor: '#09090B' }}>
        {imageSrc && (
          <img
            src={imageSrc}
            alt={title}
            style={{ width: '100%', borderRadius: 8, display: 'block' }}
          />
        )}
      </div>
    </div>
  );
};
