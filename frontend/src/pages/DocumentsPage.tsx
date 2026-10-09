import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { BookOpenText, Check, Database, LoaderCircle, Plus, Save, Trash2, X } from 'lucide-react'
import { useMemo, useState } from 'react'
import { api } from '../lib/api'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardHeader } from '../components/ui/card'
import { Textarea } from '../components/ui/textarea'

const MAX_LENGTH = 4000

type Draft = { id: string; text: string }
const newDraft = (): Draft => ({ id: crypto.randomUUID(), text: '' })

function dateLabel(value: string) {
  return new Intl.DateTimeFormat('uz-UZ', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value))
}

export function DocumentsPage() {
  const queryClient = useQueryClient()
  const [drafts, setDrafts] = useState<Draft[]>([newDraft()])
  const [successCount, setSuccessCount] = useState<number | null>(null)
  const documents = useQuery({ queryKey: ['documents'], queryFn: api.listDocuments })
  const validTexts = useMemo(() => drafts.map((item) => item.text.trim()).filter(Boolean), [drafts])
  const hasInvalid = drafts.some((item) => item.text.length > MAX_LENGTH)

  const addMutation = useMutation({
    mutationFn: () => api.addDocuments(validTexts),
    onSuccess: async (result) => {
      setSuccessCount(result.added)
      setDrafts([newDraft()])
      await queryClient.invalidateQueries({ queryKey: ['documents'] })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: api.deleteDocument,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['documents'] }),
  })

  const updateDraft = (id: string, text: string) => {
    setSuccessCount(null)
    setDrafts((current) => current.map((item) => item.id === id ? { ...item, text } : item))
  }

  return (
    <div className="space-y-8">
      <section className="grid gap-6 lg:grid-cols-[1fr_auto] lg:items-end">
        <div>
          <div className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.18em] text-cyan-300">
            <BookOpenText className="size-4" /> Knowledge base
          </div>
          <h1 className="max-w-3xl text-4xl font-bold tracking-[-0.045em] text-white sm:text-5xl">Qidiruv bazasini matnlar bilan boyiting.</h1>
          <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-400">Har bir matn Qwen3 orqali 1024 o‘lchamli vektorga aylanadi va Qdrant’da saqlanadi. Bir so‘rovda bir nechta matn qo‘shishingiz mumkin.</p>
        </div>
        <div className="flex min-w-44 items-center gap-3 rounded-2xl border border-white/[0.08] bg-white/[0.035] px-5 py-4">
          <div className="grid size-10 place-items-center rounded-xl bg-cyan-400/10 text-cyan-300"><Database className="size-5" /></div>
          <div><div className="text-2xl font-bold text-white">{documents.data?.total ?? '—'}</div><div className="text-xs text-slate-500">bazadagi matn</div></div>
        </div>
      </section>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1.05fr)_minmax(420px,.95fr)]">
        <Card>
          <CardHeader>
            <div><h2 className="font-semibold text-white">Yangi matnlar</h2><p className="mt-1 text-xs text-slate-500">Har bir maydon maksimum {MAX_LENGTH.toLocaleString()} belgi</p></div>
            <span className="rounded-lg bg-white/[0.05] px-2.5 py-1 text-xs font-semibold text-slate-400">{drafts.length} ta</span>
          </CardHeader>
          <CardContent className="space-y-4">
            {drafts.map((draft, index) => {
              const overLimit = draft.text.length > MAX_LENGTH
              return (
                <div key={draft.id} className="rounded-2xl border border-white/[0.07] bg-white/[0.025] p-3.5">
                  <div className="mb-2.5 flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-400">Matn {index + 1}</span>
                    {drafts.length > 1 && <Button variant="ghost" size="icon" onClick={() => setDrafts((items) => items.filter((item) => item.id !== draft.id))} aria-label="Matnni olib tashlash"><X /></Button>}
                  </div>
                  <Textarea value={draft.text} onChange={(event) => updateDraft(draft.id, event.target.value)} placeholder="Qidiruv bazasiga qo‘shiladigan matnni kiriting…" className={overLimit ? 'border-rose-400/50 focus:border-rose-400/60' : ''} />
                  <div className={`mt-2 text-right text-[11px] ${overLimit ? 'font-semibold text-rose-300' : 'text-slate-600'}`}>{draft.text.length.toLocaleString()} / {MAX_LENGTH.toLocaleString()}</div>
                </div>
              )
            })}

            <div className="flex flex-col gap-3 border-t border-white/[0.07] pt-4 sm:flex-row sm:justify-between">
              <Button variant="secondary" onClick={() => setDrafts((items) => [...items, newDraft()])}><Plus /> Yana matn</Button>
              <Button disabled={!validTexts.length || hasInvalid || addMutation.isPending} onClick={() => addMutation.mutate()}>
                {addMutation.isPending ? <LoaderCircle className="animate-spin" /> : <Save />}
                {validTexts.length ? `${validTexts.length} ta matnni saqlash` : 'Matnni saqlash'}
              </Button>
            </div>
            {addMutation.error && <div className="rounded-xl border border-rose-400/15 bg-rose-400/[0.07] p-3 text-xs text-rose-300">{addMutation.error.message}</div>}
            {successCount !== null && <div className="flex items-center gap-2 rounded-xl border border-emerald-400/15 bg-emerald-400/[0.07] p-3 text-xs text-emerald-300"><Check className="size-4" /> {successCount} ta matn muvaffaqiyatli qo‘shildi.</div>}
          </CardContent>
        </Card>

        <Card className="overflow-hidden">
          <CardHeader><div><h2 className="font-semibold text-white">Saqlangan matnlar</h2><p className="mt-1 text-xs text-slate-500">Qdrant collection tarkibi</p></div></CardHeader>
          <div className="max-h-[720px] overflow-y-auto">
            {documents.isPending && <div className="grid min-h-48 place-items-center text-slate-500"><LoaderCircle className="animate-spin" /></div>}
            {documents.error && <div className="m-5 rounded-xl bg-rose-400/[0.07] p-4 text-xs text-rose-300">{documents.error.message}</div>}
            {documents.data?.items.length === 0 && <div className="grid min-h-52 place-items-center px-8 text-center"><div><Database className="mx-auto mb-3 size-7 text-slate-700" /><p className="text-sm text-slate-400">Baza hozircha bo‘sh</p><p className="mt-1 text-xs text-slate-600">Birinchi matnni chapdagi forma orqali qo‘shing.</p></div></div>}
            {documents.data?.items.map((item, index) => (
              <article key={item.id} className="group flex gap-3 border-b border-white/[0.06] p-5 last:border-0 hover:bg-white/[0.02]">
                <span className="mt-0.5 grid size-7 shrink-0 place-items-center rounded-lg bg-violet-400/10 text-[10px] font-bold text-violet-300">{index + 1}</span>
                <div className="min-w-0 flex-1"><p className="line-clamp-3 text-sm leading-6 text-slate-300">{item.text}</p><p className="mt-2 text-[10px] uppercase tracking-wider text-slate-600">{dateLabel(item.created_at)}</p></div>
                <Button variant="ghost" size="icon" className="shrink-0 opacity-50 hover:text-rose-300 group-hover:opacity-100" disabled={deleteMutation.isPending} onClick={() => deleteMutation.mutate(item.id)} aria-label="O‘chirish"><Trash2 /></Button>
              </article>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}
