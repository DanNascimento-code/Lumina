import { ArrowDown, ArrowRight, MessageCircleMore, ShieldCheck, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'
import { useI18n } from '../i18n'

type Props = { onAskLumi: (prompt?: string) => void }

export function Hero({ onAskLumi }: Props) {
  const { t } = useI18n()
  return <section className="hero" id="top">
    <div className="hero-image" />
    <div className="hero-vignette" />
    <motion.div className="hero-content" initial={{ opacity: 0, y: 28 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .7 }}>
      <div className="eyebrow"><Sparkles size={15} /> {t('hero.eyebrow')}</div>
      <h1>{t('hero.title1')}<br /><em>{t('hero.title2')}</em></h1>
      <p>{t('hero.body1')}<br />{t('hero.body2')}</p>
      <div className="hero-actions">
        <a className="btn btn-light" href="#products">{t('hero.explore')} <ArrowRight size={18} /></a>
        <button className="btn btn-glass" onClick={() => onAskLumi()}><MessageCircleMore size={18} /> {t('hero.ask')}</button>
      </div>
      <div className="hero-proof">
        <span className="avatars"><i>L</i><i>M</i><i>R</i></span>
        <span><b>4.9</b> {t('hero.rating')}</span>
        <span className="proof-line" />
        <span><ShieldCheck size={17} /> {t('hero.protected')}</span>
      </div>
    </motion.div>
    <a className="scroll-cue" href="#products"><span>{t('hero.discover')}</span><ArrowDown /></a>
    <button className="hero-lumi-card" onClick={() => onAskLumi()}>
      <span className="lumi-orb small"><i /></span>
      <span><b>{t('hero.lumi')}</b><small>{t('hero.lumiBody')}</small></span>
      <ArrowRight size={18} />
    </button>
  </section>
}
