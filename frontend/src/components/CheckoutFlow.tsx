import { Check, CheckCircle2, ChevronLeft, CreditCard, LockKeyhole, QrCode, ShieldCheck, X } from 'lucide-react'
import { AnimatePresence, motion } from 'framer-motion'
import { type FormEvent, useState } from 'react'
import type { CartItem } from '../types'
import { submitCheckout } from '../lib/api'
import { formatCurrency } from '../lib/format'
import { useI18n } from '../i18n'

type Props = { open: boolean; items: CartItem[]; subtotal: number; onClose: () => void; onSuccess: () => void }
type Payment = 'credit_card' | 'pix'
type CustomerDetails = { name: string; email: string; postalCode: string; street: string; number: string; complement: string; city: string; state: string }

const emptyCustomer: CustomerDetails = { name: '', email: '', postalCode: '', street: '', number: '', complement: '', city: '', state: '' }

export function CheckoutFlow({ open, items, subtotal, onClose, onSuccess }: Props) {
  const { locale, t } = useI18n()
  const [step, setStep] = useState(1)
  const [payment, setPayment] = useState<Payment>('credit_card')
  const [loading, setLoading] = useState(false)
  const [customer, setCustomer] = useState<CustomerDetails>(emptyCustomer)
  const [order, setOrder] = useState<{ code: string; estimated_delivery: string } | null>(null)
  const shipping = subtotal >= 499 ? 0 : 24.9

  const saveDelivery = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    setCustomer({
      name: String(data.get('name')), email: String(data.get('email')), postalCode: String(data.get('postal_code')),
      street: String(data.get('street')), number: String(data.get('number')), complement: String(data.get('complement') || ''),
      city: String(data.get('city')), state: String(data.get('state')),
    })
    setStep(2)
  }

  const complete = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); setLoading(true)
    const payload = {
      customer_name: customer.name, customer_email: customer.email, payment_method: payment,
      items: items.map((item) => ({ product_id: item.id, quantity: item.quantity })),
      address: { postal_code: customer.postalCode, street: customer.street, number: customer.number, complement: customer.complement, city: customer.city, state: customer.state },
    }
    try {
      const result = await submitCheckout(payload)
      setOrder(result)
      onSuccess()
      setStep(3)
    } catch {
      setLoading(false)
    } finally { setLoading(false) }
  }

  const close = () => {
    onClose()
    setTimeout(() => { setStep(1); setOrder(null); setCustomer(emptyCustomer); setPayment('credit_card') }, 300)
  }

  const total = subtotal + shipping
  return <AnimatePresence>{open && <motion.div className="checkout-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
    <motion.div className="checkout-shell" initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: 20, opacity: 0 }}>
      <div className="checkout-top"><button onClick={step === 2 ? () => setStep(1) : close}>{step === 2 ? <ChevronLeft /> : <X />}</button><span className="brand compact"><span className="brand-mark"><i /><i /></span><b>LUMINA</b></span><span><LockKeyhole size={14} /> {t('checkout.secure')}</span></div>
      <div className="checkout-steps"><span className={step >= 1 ? 'active' : ''}><i>{step > 1 ? <Check /> : 1}</i> {t('checkout.identification')}</span><b /><span className={step >= 2 ? 'active' : ''}><i>{step > 2 ? <Check /> : 2}</i> {t('checkout.payment')}</span><b /><span className={step >= 3 ? 'active' : ''}><i>3</i> {t('checkout.confirmation')}</span></div>

      {step === 1 && <div className="checkout-grid"><form className="checkout-form" onSubmit={saveDelivery}><small>{t('checkout.step1')}</small><h2>{t('checkout.where')}</h2><p>{t('checkout.whereBody')}</p>
        <div className="field-grid"><label className="full">{t('checkout.name')}<input name="name" autoComplete="name" required /></label><label className="full">{t('checkout.email')}<input name="email" type="email" autoComplete="email" required /></label><label>{t('checkout.postal')}<input name="postal_code" autoComplete="postal-code" required /></label><label>{t('checkout.state')}<input name="state" maxLength={2} autoComplete="address-level1" required /></label><label className="wide">{t('checkout.address')}<input name="street" autoComplete="street-address" required /></label><label>{t('checkout.number')}<input name="number" required /></label><label className="full">{t('checkout.complement')}<input name="complement" placeholder={t('checkout.complementHint')} /></label><label className="wide">{t('checkout.city')}<input name="city" autoComplete="address-level2" required /></label></div>
        <button className="btn btn-primary wide" type="submit">{t('checkout.continue')} →</button>
      </form><OrderSummary items={items} subtotal={subtotal} shipping={shipping} /></div>}

      {step === 2 && <form className="checkout-grid" onSubmit={complete}><div className="checkout-form"><small>{t('checkout.step2')}</small><h2>{t('checkout.howPay')}</h2>
        <div className="payment-tabs"><button type="button" className={payment === 'credit_card' ? 'active' : ''} onClick={() => setPayment('credit_card')}><CreditCard /> {t('checkout.card')}</button><button type="button" className={payment === 'pix' ? 'active' : ''} onClick={() => setPayment('pix')}><QrCode /> {t('checkout.pix')} <i>{t('checkout.pixOffer')}</i></button></div>
        {payment === 'credit_card' ? <div className="field-grid payment-fields"><label className="full">{t('checkout.cardNumber')}<input inputMode="numeric" autoComplete="cc-number" placeholder="0000 0000 0000 0000" required /></label><label className="full">{t('checkout.cardName')}<input autoComplete="cc-name" required /></label><label>{t('checkout.expiry')}<input autoComplete="cc-exp" placeholder="MM/YY" required /></label><label>CVV<input inputMode="numeric" autoComplete="cc-csc" placeholder="000" required /></label><label className="full">{t('checkout.installments')}<select defaultValue="10"><option value="1">1x {formatCurrency(total, locale)}</option><option value="10">10x {formatCurrency(total / 10, locale)}</option></select></label></div> : <div className="pix-box"><span><QrCode /></span><h3>{t('checkout.pixTitle')}</h3><p>{t('checkout.pixBody')}</p></div>}
        <button className="btn btn-primary wide" disabled={loading}>{loading ? <span className="spinner" /> : <LockKeyhole size={17} />} {loading ? t('checkout.processing') : t('checkout.pay', { value: formatCurrency(total, locale) })}</button>
        <div className="secure-note"><ShieldCheck /> {t('checkout.paymentPrivacy')}</div>
      </div><OrderSummary items={items} subtotal={subtotal} shipping={shipping} /></form>}

      {step === 3 && <div className="success-screen"><motion.span initial={{ scale: .4 }} animate={{ scale: 1 }} className="success-icon"><CheckCircle2 /></motion.span><small>{t('checkout.approved')}</small><h2>{t('checkout.successTitle', { name: customer.name.split(' ')[0] || customer.name })}</h2><p>{t('checkout.successBody', { code: order?.code ?? '' })}</p><div className="delivery-card"><span>{t('checkout.eta')}</span><b>{formatDeliveryDate(order?.estimated_delivery, locale)}</b><i><span /></i><div><em><Check /> {t('checkout.paid')}</em><em><Check /> {t('checkout.preparing')}</em><em>{t('checkout.transit')}</em></div></div><button className="btn btn-primary" onClick={close}>{t('checkout.continueShopping')}</button><span className="success-email">{t('checkout.emailSent', { email: customer.email })}</span></div>}
    </motion.div>
  </motion.div>}</AnimatePresence>
}

function formatDeliveryDate(isoDate: string | undefined, locale: string) {
  const value = isoDate ?? new Date(Date.now() + 5 * 86400000).toISOString().slice(0, 10)
  return new Date(`${value.slice(0, 10)}T12:00:00`).toLocaleDateString(locale, { weekday: 'long', day: '2-digit', month: 'long' })
}

function OrderSummary({ items, subtotal, shipping }: { items: CartItem[]; subtotal: number; shipping: number }) {
  const { locale, t } = useI18n()
  return <aside className="order-summary"><span>{t('checkout.summary')}</span><div className="summary-items">{items.map((item) => <div key={item.id}><img src={item.image_url} alt="" /><p><b>{item.name}</b><span>{t('checkout.qty', { count: item.quantity })}</span></p><strong>{formatCurrency(item.price * item.quantity, locale)}</strong></div>)}</div><div className="summary-lines"><p><span>{t('cart.subtotal')}</span><b>{formatCurrency(subtotal, locale)}</b></p><p><span>{t('cart.shipping')}</span><b className="free">{shipping ? formatCurrency(shipping, locale) : t('cart.free')}</b></p><p className="total"><span>{t('checkout.total')}</span><b>{formatCurrency(subtotal + shipping, locale)}</b></p></div><small><ShieldCheck /> {t('checkout.protected')}</small></aside>
}
