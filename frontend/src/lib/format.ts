export const formatCurrency = (value: number, locale = 'en-US') => new Intl.NumberFormat(locale, {
  style: 'currency', currency: 'BRL', currencyDisplay: 'narrowSymbol',
}).format(value)
