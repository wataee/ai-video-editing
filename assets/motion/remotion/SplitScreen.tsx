import React from 'react';
import { Video, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface SplitScreenProps {
  speakerVideoSrc: string;
  speakerStartTimeSec?: number;
  bottomContent: React.ReactNode;
  splitRatio?: number; 
  dividerColor?: string;
}


export const SplitScreen: React.FC<SplitScreenProps> = ({
  speakerVideoSrc,
  speakerStartTimeSec = 0,
  bottomContent,
  splitRatio = 0.52,
  dividerColor = 'rgba(255, 255, 255, 0.15)',
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const slideUp = spring({
    frame,
    fps,
    config: {
      damping: 15,
      mass: 0.8,
      stiffness: 120,
    },
  });

  const bottomOffsetY = interpolate(slideUp, [0, 1], [300, 0]);
  const bottomOpacity = interpolate(slideUp, [0, 0.4], [0, 1], { extrapolateRight: 'clamp' });

  const topHeight = height * splitRatio;
  const bottomHeight = height * (1 - splitRatio);

  return (
    <div
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        backgroundColor: '#09090B',
        overflow: 'hidden',
      }}
    >
      {}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: topHeight,
          overflow: 'hidden',
        }}
      >
        <Video
          src={speakerVideoSrc}
          startFrom={Math.round(speakerStartTimeSec * fps)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: 'center 20%',
          }}
        />
      </div>

      {}
      <div
        style={{
          position: 'absolute',
          top: topHeight - 1,
          left: 0,
          width: '100%',
          height: 2,
          backgroundColor: dividerColor,
          zIndex: 10,
        }}
      />

      {}
      <div
        style={{
          position: 'absolute',
          top: topHeight,
          left: 0,
          width: '100%',
          height: bottomHeight,
          transform: `translateY(${bottomOffsetY}px)`,
          opacity: bottomOpacity,
          padding: 40,
          boxSizing: 'border-box',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: '#0C0D0E',
          overflow: 'hidden',
        }}
      >
        {bottomContent}
      </div>
    </div>
  );
};
