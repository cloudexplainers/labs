from datetime import datetime

import excel, invoices, portal, report, send, stock, tidy

print("shop-bot started", datetime.now().strftime("%Y-%m-%d %H:%M"))
for step in [tidy, report, excel, invoices, stock, portal, send]:
    print("==", step.__name__)
    step.run()
print("shop-bot done")
