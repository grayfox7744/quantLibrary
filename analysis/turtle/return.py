import utility.windutility as wu
from datetime import date
import seaborn as sns

today = date.today()
startdate = wu.tdaysoffset(-120, today)
enddate = wu.tdaysoffset(-1, today)

bars = wu.wsd('000001.SH','open, close', startdate, enddate)
bars['return'] = bars.close / bars.open - 1
sns.distplot(bars['return'])