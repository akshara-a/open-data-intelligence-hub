import sys, glob, os
ROUTES=["POST /auth/login","GET /auth/validate","POST /v2/auth/token","GET /orders/{id}","POST /orders","GET /users/{id}","POST /payments/charge","POST /notifications/send","POST /inventory/reserve"]
FRONT=["web-login-page","web-checkout-page","mobile-app-auth","customer-portal"]
MODS=["legacy-token-validator","session-manager","gateway-router","order-processing-module","user-profile-module","payment-processor","email-dispatcher","stock-manager"]
SVCS=["api-gateway","auth-service-v2","inventory-service","legacy-auth-service","notification-service","order-service","payment-service","user-service"]
path=sys.argv[1] if len(sys.argv)>1 else max(glob.glob("reports/*legacy-auth-module*.md"),key=os.path.getmtime)
md=open(path).read().split("## Appendix A")[0]
print("report:",path)
for name,items in [("API routes",ROUTES),("Frontend",FRONT),("Modules",MODS),("Services",SVCS)]:
    miss=[i for i in items if i not in md]
    print(f"{name:11} {len(items)-len(miss)}/{len(items)}", "OK" if not miss else f"MISSING {miss}")
print("Section headings present:", {k:(k.lower() in md.lower()) for k in ["architectural debt","refactoring"]})