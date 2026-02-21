import { useEffect } from 'react';

export const Failsafe = () => {
  useEffect(() => {
    const handleKeyDown = (event) => {
      // The secret trigger: Ctrl + Shift + O
      if (event.ctrlKey && event.shiftKey && event.key === 'O') {
        event.preventDefault(); // Stops the browser from doing weird things
        
        console.warn("🚨 WIZARD OF OZ OVERRIDE ENGAGED! 🚨");
        
        // Visual feedback just for you so you know you pressed it right during testing
        alert("MANUAL OVERRIDE SIGNAL SENT TO BACKEND");

        // This is the fetch request your backend friend will catch!
        fetch('http://localhost:8000/api/override', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'force_phase_change' })
        }).catch(() => {
          // We expect a fetch error right now because your friend's backend isn't running yet!
          console.log("Waiting for backend API to be ready...");
        });
      }
    };

    // Attach the listener to the whole browser window
    window.addEventListener('keydown', handleKeyDown);

    // Clean it up if the component unmounts
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // This component is completely invisible to the judges!
  return null; 
};