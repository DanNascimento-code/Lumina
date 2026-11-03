export const USD_PER_BRL = 0.18

export const formatCurrency = (valueInBrl: number, locale = 'en-US') => {
  const usesBrl = locale === 'pt-BR'
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: usesBrl ? 'BRL' : 'USD',
    currencyDisplay: 'narrowSymbol',
  }).format(usesBrl ? valueInBrl : valueInBrl * USD_PER_BRL)
}
