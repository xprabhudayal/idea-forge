import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingOverlayProps {
    isVisible: boolean;
    message: string;
}

export function LoadingOverlay({ isVisible, message }: LoadingOverlayProps) {
    if (!isVisible) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm transition-opacity duration-300">
            <div className="flex flex-col items-center justify-center space-y-6 max-w-md text-center p-6 rounded-lg">
                <Loader2 className="h-16 w-16 text-primary animate-spin" />
                <h2 className="text-2xl font-semibold tracking-tight animate-pulse text-foreground">
                    {message}
                </h2>
            </div>
        </div>
    );
}
