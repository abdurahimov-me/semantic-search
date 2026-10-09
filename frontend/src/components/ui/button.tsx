import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-semibold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400/30 disabled:pointer-events-none disabled:opacity-45 [&_svg]:size-4',
  {
    variants: {
      variant: {
        default: 'bg-slate-200 text-slate-950 hover:bg-white',
        secondary: 'border border-white/10 bg-white/[0.055] text-slate-200 hover:bg-white/[0.09]',
        ghost: 'text-slate-400 hover:bg-white/[0.06] hover:text-white',
        danger: 'bg-rose-500/10 text-rose-300 hover:bg-rose-500/20',
      },
      size: {
        default: 'h-11 px-4',
        sm: 'h-9 rounded-lg px-3 text-xs',
        icon: 'size-9 rounded-lg',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  },
)

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

export function Button({ className, variant, size, asChild, ...props }: ButtonProps) {
  const Component = asChild ? Slot : 'button'
  return <Component className={cn(buttonVariants({ variant, size }), className)} {...props} />
}
