import { useState, useCallback } from 'react';
import { ChatState, StreamChunk } from '@/types/chat';
import { streamChatCompletion, ApiError } from '@/lib/api';

export function useChat() {
  const [state, setState] = useState<ChatState>({
    text: '',
    response: '',
    isStreaming: false,
    error: null,
    responseVisible: false,
    usage: null,
    model: '',
  });

  const [isPanelOpen, setIsPanelOpen] = useState(false);

  const updateState = useCallback((updates: Partial<ChatState>) => {
    setState(prev => ({ ...prev, ...updates }));
  }, []);

  const handleTextChange = useCallback((value: string) => {
    updateState({
      text: value,
      error: null,
    });
  }, [updateState]);

  const streamResponse = useCallback(async (message: string) => {
    console.log('Starting stream response for:', message);
    
    // Open the side panel and reset state
    setIsPanelOpen(true);
    updateState({
      isStreaming: true,
      response: '',
      error: null,
      responseVisible: true,
      usage: null,
      model: '',
    });

    let fullContent = '';

    await streamChatCompletion({
      message: message.trim(),
      onChunk: (chunk: StreamChunk) => {
        console.log('Received chunk:', chunk);
        if (chunk.content) {
          fullContent += chunk.content;
          console.log('Updated full content:', fullContent);
          updateState({
            response: fullContent,
            model: chunk.model,
          });
        }

        if (chunk.is_complete) {
          console.log('Stream completed, final usage:', chunk.usage);
          updateState({
            usage: chunk.usage || null,
            isStreaming: false,
          });
        }
      },
      onComplete: () => {
        console.log('Stream complete callback triggered');
        updateState({
          isStreaming: false,
        });
      },
      onError: (error: ApiError) => {
        console.error('Stream error:', error);
        updateState({
          error: error.message,
          isStreaming: false,
          responseVisible: false,
        });
        // Keep panel open to show error
      },
    });
  }, [updateState]);

  const closeSidePanel = useCallback(() => {
    setIsPanelOpen(false);
  }, []);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();

    if (!state.text.trim()) {
      updateState({ error: 'Please enter some text' });
      return;
    }

    if (state.isStreaming) {
      return;
    }

    try {
      await streamResponse(state.text.trim());
    } catch (err) {
      updateState({
        error: err instanceof Error ? err.message : 'An error occurred',
        responseVisible: false,
      });
    }
  }, [state.text, state.isStreaming, streamResponse, updateState]);

  return {
    ...state,
    isPanelOpen,
    handleTextChange,
    handleSubmit,
    streamResponse,
    closeSidePanel,
  };
}