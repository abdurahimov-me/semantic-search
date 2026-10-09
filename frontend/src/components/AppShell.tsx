import { Link, Outlet, useRouterState } from '@tanstack/react-router'
import { Braces, Database, FlaskConical, Sparkles } from 'lucide-react'
import { cn } from '../lib/utils'

const navigation = [
  { to: '/', label: 'Matnlar bazasi', icon: Database },
  { to: '/test', label: 'Qidiruv testi', icon: FlaskConical },
] as const

export function AppShell() {
  const pathname = useRouterState({ select: (state) => state.location.pathname })

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-white/[0.07] bg-[#070b14]/80 backdrop-blur-2xl">
        <div className="mx-auto flex h-18 max-w-[1440px] items-center justify-between px-5 lg:px-8">
          <Link to="/" className="flex items-center gap-3 text-white no-underline">
            <div className="grid size-10 place-items-center rounded-xl bg-gradient-to-br from-cyan-300 to-violet-500 text-slate-950 shadow-lg shadow-cyan-500/15">
              <Braces className="size-5" />
            </div>
            <div>
              <div className="text-sm font-bold tracking-tight">Semantic Lab</div>
              <div className="mt-0.5 text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">Qwen · Qdrant</div>
            </div>
          </Link>

          <nav className="flex items-center gap-1 rounded-xl border border-white/[0.07] bg-white/[0.035] p-1">
            {navigation.map((item) => {
              const active = item.to === '/' ? pathname === '/' : pathname.startsWith(item.to)
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={cn(
                    'flex items-center gap-2 rounded-lg px-3.5 py-2 text-xs font-semibold text-slate-500 transition-all',
                    active && 'bg-white/[0.09] text-white shadow-sm',
                  )}
                >
                  <item.icon className="size-3.5" />
                  <span className="hidden sm:inline">{item.label}</span>
                </Link>
              )
            })}
          </nav>

          <div className="hidden items-center gap-2 text-xs text-slate-500 md:flex">
            <Sparkles className="size-3.5 text-cyan-300" />
            Qwen3 0.6B
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-[1440px] px-5 py-10 lg:px-8 lg:py-14">
        <Outlet />
      </main>
    </div>
  )
}
