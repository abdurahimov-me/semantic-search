import * as React from 'react'
import { cn } from '../../lib/utils'

export function Textarea({ className, ...props }: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={cn('min-h-32 w-full resize-y rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm leading-6 text-slate-100 outline-none placeholder:text-slate-600 focus:border-slate-400/40 focus:ring-4 focus:ring-slate-400/[0.05]', className)}
      {...props}
    />
  )
}
