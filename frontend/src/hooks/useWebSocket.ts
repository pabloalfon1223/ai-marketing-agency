import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { wsClient } from '../api/websocket';

export function useWebSocket() {
  const queryClient = useQueryClient();

  useEffect(() => {
    wsClient.connect();

    const unsub = wsClient.subscribe((data) => {
      if (data.type === 'task_update') {
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['agents-status'] });
        queryClient.invalidateQueries({ queryKey: ['analytics'] });
      }
      if (data.type === 'content_update') {
        queryClient.invalidateQueries({ queryKey: ['content'] });
      }
    });

    return () => {
      unsub();
      wsClient.disconnect();
    };
  }, [queryClient]);
}
