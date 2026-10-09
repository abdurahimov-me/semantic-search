import { useMutation } from '@tanstack/react-query'
import { ArrowRight, LoaderCircle, Search } from 'lucide-react'
import { useState } from 'react'
import { api, type SearchResult } from '../lib/api'
import { Button } from '../components/ui/button'
import { Card, CardContent } from '../components/ui/card'
import { Textarea } from '../components/ui/textarea'

const MAX_LENGTH = 4000

function scoreTone(score: number) {
  if (score >= 80) return { label: 'Juda o‘xshash', text: 'text-slate-200', bar: 'from-slate-300 to-slate-400', dot: 'bg-slate-300' }
  if (score >= 60) return { label: 'O‘xshash', text: 'text-slate-300', bar: 'from-slate-400 to-slate-500', dot: 'bg-slate-400' }
  if (score >= 40) return { label: 'Qisman o‘xshash', text: 'text-slate-400', bar: 'from-slate-500 to-slate-600', dot: 'bg-slate-500' }
  return { label: 'Past o‘xshashlik', text: 'text-slate-400', bar: 'from-slate-500 to-slate-400', dot: 'bg-slate-500' }
}

function ResultCard({ result, index }: { result: SearchResult; index: number }) {
  const tone = scoreTone(result.score_percent)
  return (
    <article className="rounded-2xl border border-white/[0.08] bg-white/[0.025] p-5 transition hover:border-white/[0.14] hover:bg-white/[0.04]">
      <div className="flex items-start gap-4">
        <div className="grid size-10 shrink-0 place-items-center rounded-xl border border-white/[0.08] bg-black/20 text-sm font-bold text-slate-400">#{index + 1}</div>
        <div className="min-w-0 flex-1">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div className={`flex items-center gap-2 text-xs font-semibold ${tone.text}`}><span className={`size-1.5 rounded-full ${tone.dot}`} />{tone.label}</div>
            <div className="flex items-baseline gap-1"><strong className="text-2xl tracking-tight text-white">{result.score_percent.toFixed(1)}</strong><span className="text-xs text-slate-500">%</span></div>
          </div>
          <div className="mb-4 h-1.5 overflow-hidden rounded-full bg-white/[0.06]"><div className={`h-full rounded-full bg-gradient-to-r ${tone.bar}`} style={{ width: `${Math.max(2, result.score_percent)}%` }} /></div>
          <p className="text-sm leading-7 text-slate-300">{result.text}</p>
          <div className="mt-4 text-[10px] uppercase tracking-[0.13em] text-slate-600">Moslik darajasi · {result.score.toFixed(4)}</div>
        </div>
      </div>
    </article>
  )
}

export function TestPage() {
  const [text, setText] = useState('')
  const searchMutation = useMutation({ mutationFn: () => api.search(text.trim()) })
  const overLimit = text.length > MAX_LENGTH

  return (
    <div className="space-y-8">
      <section>
        <div className="mb-3 flex items-center gap-2 text-xs font-semibold text-slate-500"><Search className="size-4" /> Semantik qidiruv moduli</div>
        <h1 className="max-w-4xl text-4xl font-bold tracking-[-0.045em] text-white sm:text-5xl">Ma’nosi yaqin matnlarni bir zumda toping.</h1>
        <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-400">Matn kiriting. Tizim bazadagi ma’nosi eng yaqin natijalarni moslik darajasi bo‘yicha tartiblaydi.</p>
      </section>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,.78fr)_minmax(0,1.22fr)]">
        <div className="space-y-5 xl:sticky xl:top-28 xl:self-start">
          <Card className="overflow-hidden">
            <CardContent className="p-6">
              <div className="mb-5 flex items-center gap-3"><div className="grid size-11 place-items-center rounded-xl bg-slate-800 text-slate-300"><Search className="size-5" /></div><div><h2 className="font-semibold text-white">Test matni</h2><p className="mt-0.5 text-xs text-slate-500">Qidiruv matnini yozing</p></div></div>
              <Textarea value={text} onChange={(event) => setText(event.target.value)} placeholder="Masalan: Yetkazib berish qancha vaqt oladi?" className={`min-h-52 bg-black/25 ${overLimit ? 'border-rose-400/50' : ''}`} onKeyDown={(event) => { if ((event.ctrlKey || event.metaKey) && event.key === 'Enter' && text.trim() && !overLimit) searchMutation.mutate() }} />
              <div className={`mt-2 text-right text-[11px] ${overLimit ? 'font-semibold text-rose-300' : 'text-slate-600'}`}>{text.length.toLocaleString()} / {MAX_LENGTH.toLocaleString()}</div>
              <Button className="mt-4 w-full" disabled={!text.trim() || overLimit || searchMutation.isPending} onClick={() => searchMutation.mutate()}>
                {searchMutation.isPending ? <LoaderCircle className="animate-spin" /> : <Search />}
                O‘xshashlarini topish <ArrowRight className="ml-auto" />
              </Button>
              <p className="mt-3 text-center text-[10px] text-slate-600">Ctrl + Enter orqali ham qidirishingiz mumkin</p>
              {searchMutation.error && <div className="mt-4 rounded-xl border border-rose-400/15 bg-rose-400/[0.07] p-3 text-xs text-rose-300">{searchMutation.error.message}</div>}
            </CardContent>
          </Card>

          <div className="rounded-2xl border border-white/[0.07] bg-white/[0.025] p-4 text-xs leading-6 text-slate-500">Natijalar matn mazmunining yaqinligiga qarab saralanadi. Yuqori foiz kuchliroq moslikni bildiradi.</div>
        </div>

        <Card className="min-h-[560px]">
          <div className="flex items-center justify-between border-b border-white/[0.07] px-6 py-5"><div><h2 className="font-semibold text-white">Natijalar</h2><p className="mt-1 text-xs text-slate-500">Eng mos natija birinchi ko‘rsatiladi</p></div>{searchMutation.data && <span className="rounded-lg bg-slate-700/40 px-2.5 py-1 text-xs font-semibold text-slate-300">{searchMutation.data.total} ta topildi</span>}</div>
          <div className="space-y-3 p-5 sm:p-6">
            {!searchMutation.data && !searchMutation.isPending && <div className="grid min-h-[420px] place-items-center text-center"><div className="max-w-xs"><div className="mx-auto mb-5 grid size-16 place-items-center rounded-2xl border border-white/[0.08] bg-white/[0.025]"><Search className="size-7 text-slate-700" /></div><h3 className="text-sm font-semibold text-slate-300">Natijalar shu yerda chiqadi</h3><p className="mt-2 text-xs leading-6 text-slate-600">Chap tomonda matn kiriting va semantic qidiruvni boshlang.</p></div></div>}
            {searchMutation.isPending && <div className="grid min-h-[420px] place-items-center text-center"><div><LoaderCircle className="mx-auto mb-4 size-7 animate-spin text-slate-300" /><p className="text-sm text-slate-400">Natijalar qidirilmoqda…</p></div></div>}
            {searchMutation.data?.results.length === 0 && <div className="grid min-h-[420px] place-items-center text-center"><div><Search className="mx-auto mb-4 size-7 text-slate-700" /><p className="text-sm text-slate-400">O‘xshash matn topilmadi</p></div></div>}
            {searchMutation.data?.results.map((result, index) => <ResultCard key={result.id} result={result} index={index} />)}
          </div>
        </Card>
      </div>
    </div>
  )
}
