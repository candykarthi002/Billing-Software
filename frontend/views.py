from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Bill
import csv
import json
from datetime import datetime
from .filters import StatementFilter, VehicleFilter, BillFilter

'''
Second Cycle Requirements:
    - Edit option ✔
    - Delete option ✔
    - Statement ✔
    - Mobile Responsive

Third Cycle Requirements:
    - Re-organize home page
    - Add Vehicle Report Page
        - Bill Date, Number and Vehicle Number
    - Add Dashboard Page
        - Bar Chart
'''


months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# Create your views here.


def home(request):
    bills = Bill.objects.all().order_by('-bill_date')
    bill_count = bills.count()
    return render(request, 'frontend/home.html', {'bills': bills[:10], "bill_count": bill_count})


def get_vehicle_report(request):
    bills = Bill.objects.all()
    myFilter = VehicleFilter(request.GET, queryset=bills)
    bills = myFilter.qs
    return render(request, 'frontend/vehicle_report.html', {'bills': bills, 'myFilter': myFilter})


def index(request):
    return render(request, 'frontend/base.html')


def get_result(request, bill_id):
    bill = Bill.objects.filter(bill_no=bill_id).first()
    bill_date = bill.bill_date.strftime('%d.%m.%Y')
    cust_name = bill.customer_name
    cust_addr_1 = bill.customer_address_line_1
    cust_addr_2 = bill.customer_address_line_2
    cust_addr_3 = bill.customer_address_line_3
    from_addr = bill.from_field
    to_addr = bill.to_field
    lr_no = bill.lr_no
    lr_date = bill.lr_date.strftime('%d.%m.%Y')
    invoice_no = bill.invoice_no
    truck_no = bill.truck_no
    container_no = bill.container_no
    be_no = bill.be_no
    freight_charges = bill.freight_charges if bill.freight_charges else ''
    hamali_charges = bill.hamali_charges if bill.hamali_charges else ''
    halting_charges = bill.halting_charges if bill.halting_charges else ''
    weight_charges = bill.weight_charges if bill.weight_charges else ''
    bill_ex_charges = bill.bill_exchange_charges if bill.bill_exchange_charges else ''
    total = bill.total
    total_in_words = convert_number_to_words(total)
    return render(request, 'frontend/result.html', {'bill_no': bill_id, "bill_date": bill_date, "cust_name": cust_name, "cust_addr_1": cust_addr_1, "cust_addr_2": cust_addr_2, "cust_addr_3": cust_addr_3, "from": from_addr, "to": to_addr, "lr_no": lr_no, "lr_date": lr_date, "invoice_no": invoice_no,  "truck_no": truck_no, "container_no": container_no, "be_no": be_no, "freight_charges": freight_charges, "hamali_charges": hamali_charges, "halting_charges": halting_charges, "weight_charges": weight_charges, "bill_ex_charges": bill_ex_charges, "total": total, "total_in_words": total_in_words})


def generate_bill(request):
    if request.method == "POST":
        bill_no = request.POST.get('bill-no')
        bill_date = request.POST.get('bill-date')
        cust_name = request.POST.get('cust-name')
        cust_addr_1 = request.POST.get('cust-addr-1')
        cust_addr_2 = request.POST.get('cust-addr-2')
        cust_addr_3 = request.POST.get('cust-addr-3')
        from_addr = request.POST.get('from').upper()
        to_addr = request.POST.get('to').upper()
        lr_no = request.POST.get('lr-no')
        lr_date = request.POST.get('lr-date')
        invoice_no = request.POST.get('invoice-no')
        truck_no = request.POST.get('truck-no')
        container_no = request.POST.get('container-no')
        be_no = request.POST.get('be-no')
        freight_charges = int(request.POST.get(
            'freight-charges') if request.POST.get('freight-charges') else 0)
        hamali_charges = int(request.POST.get(
            'hamali-charges') if request.POST.get('hamali-charges') else 0)
        halting_charges = int(request.POST.get(
            'halting-charges') if request.POST.get('halting-charges') else 0)
        weight_charges = int(request.POST.get(
            'weight-charges') if request.POST.get('weight-charges') else 0)
        bill_ex_charges = int(request.POST.get(
            'bill-ex-charges') if request.POST.get('bill-ex-charges') else 0)
        total = sum([freight_charges, hamali_charges,
                    halting_charges, weight_charges, bill_ex_charges])
        bill = Bill(bill_no=bill_no, bill_date=bill_date, customer_name=cust_name, customer_address_line_1=cust_addr_1,  customer_address_line_2=cust_addr_2,  customer_address_line_3=cust_addr_3, from_field=from_addr, to_field=to_addr, lr_no=lr_no, lr_date=lr_date, invoice_no=invoice_no, truck_no=truck_no,
                    container_no=container_no, be_no=be_no, freight_charges=freight_charges, hamali_charges=hamali_charges, halting_charges=halting_charges, weight_charges=weight_charges, bill_exchange_charges=bill_ex_charges, total=total)
        bill.save()
        return HttpResponseRedirect(f'/result/{bill_no}')


def edit_bill(request, bill_id):
    if request.method == 'POST':
        bill = Bill.objects.filter(bill_no=bill_id).first()
        bill.bill_date = request.POST.get('bill-date')
        bill.customer_name = request.POST.get('cust-name')
        bill.customer_address_line_1 = request.POST.get('cust-addr-1')
        bill.customer_address_line_2 = request.POST.get('cust-addr-2')
        bill.customer_address_line_3 = request.POST.get('cust-addr-3')
        bill.from_field = request.POST.get('from').upper()
        bill.to_field = request.POST.get('to').upper()
        bill.lr_no = request.POST.get('lr-no')
        bill.lr_date = request.POST.get('lr-date')
        bill.invoice_no = request.POST.get('invoice-no')
        bill.truck_no = request.POST.get('truck-no')
        bill.container_no = request.POST.get('container-no')
        bill.be_no = request.POST.get('be-no')
        freight_charges = int(request.POST.get(
            'freight-charges') if request.POST.get('freight-charges') else 0)
        hamali_charges = int(request.POST.get(
            'hamali-charges') if request.POST.get('hamali-charges') else 0)
        halting_charges = int(request.POST.get(
            'halting-charges') if request.POST.get('halting-charges') else 0)
        weight_charges = int(request.POST.get(
            'weight-charges') if request.POST.get('weight-charges') else 0)
        bill_ex_charges = int(request.POST.get(
            'bill-ex-charges') if request.POST.get('bill-ex-charges') else 0)
        bill.freight_charges = freight_charges
        bill.hamali_charges = hamali_charges
        bill.halting_charges = halting_charges
        bill.weight_charges = weight_charges
        bill.bill_exchange_charges = bill_ex_charges
        bill.total = sum([freight_charges, hamali_charges,
                          halting_charges, weight_charges, bill_ex_charges])
        bill.save()
        return HttpResponseRedirect(f'/result/{bill_id}')
    bill = Bill.objects.filter(bill_no=bill_id).first()
    return render(request, 'frontend/base.html', {'bill': bill})


def delete_bill(request, bill_id):
    bill = Bill.objects.filter(bill_no=bill_id).first()
    if bill:
        bill.delete()
    return HttpResponseRedirect('/')


# currency conversion

def convert_number_to_words(number):
    # Word equivalents for numbers from 0 to 19 and multiples of 10 up to 90
    ones = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
            'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = ['', '', 'twenty', 'thirty', 'forty',
            'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

    def convert_group_to_words(group):
        hundred_word = ''
        ten_word = ''
        one_word = ''

        if group // 100 > 0:
            hundred_word = ones[group // 100] + ' hundred '
            group %= 100

        if group // 10 > 1:
            ten_word = tens[group // 10] + ' '
            group %= 10

        if 0 < group < 20:
            one_word = ones[group]

        return hundred_word + ten_word + one_word

    if number == 0:
        return "zero rupees"

    result = ''
    groups = []
    while number > 0:
        groups.append(number % 1000)
        number //= 1000

    magnitudes = ['', ' thousand', 'million', 'billion', 'trillion',
                  'quadrillion', 'quintillion']  # Add more if needed

    for i, group in enumerate(groups):
        if group != 0:
            result = convert_group_to_words(
                group) + magnitudes[i] + ' ' + result

    return result.strip().capitalize() + ' rupees'


def get_statement(request):
    bills = Bill.objects.all()
    myFilter = StatementFilter(request.GET, queryset=bills)
    bills = myFilter.qs.order_by("customer_name", "from_field", "to_field")
    customers = myFilter.qs.values_list(
        'customer_name', flat=True).distinct()
    customer_name = ""
    dataset = {}
    cust_total = {}
    # if customers.count() > 1:
    for c in customers:
        dataset[c] = bills.filter(customer_name=c)
        total = 0
        for b in dataset[c]:
            total += b.total
        cust_total[c] = total

    if request.method == "POST":
        data = {}
        for k, v in dataset.items():
            # data = json.dumps()
            data[k] = []
            for val in v:
                data[k].append({'lr_no': val.lr_no, 'lr_date': val.lr_date.strftime('%d/%m%Y'), 'bill_no': val.bill_no,
                               'bill_date': val.bill_date.strftime('%d/%m%Y'), 'from': val.from_field, 'to': val.to_field, 'total': val.total})
        data = json.dumps(data)
        return redirect(f'/export-csv/statement/?data={data}')

    # print(dataset)
    return render(request, 'frontend/statement.html', {"bills": dataset, 'customer_name': customer_name, 'totals': cust_total, "myFilter": myFilter})


def get_statistics(request):
    bills = Bill.objects.all()
    amounts = {}
    for month in months:
        amounts[month] = 0
    for bill in bills:
        # print(months[bill.bill_date.month])
        amounts[months[bill.bill_date.month]] += bill.total
    print(amounts)
    return render(request, 'frontend/statistics.html', {'bills': bills, 'amounts': amounts})


def get_all_bills(request):
    bills = Bill.objects.all()
    myFilter = BillFilter(request.GET, queryset=bills)
    bills = myFilter.qs
    bill_count = bills.count()
    if request.method == "POST":
        data = []
        for bill in bills:
            data.append({'lr_no': bill.lr_no, 'lr_date': bill.lr_date.strftime('%d/%m%Y'), 'bill_no': bill.bill_no,
                         'bill_date': bill.bill_date.strftime('%d/%m%Y'), 'from': bill.from_field, 'to': bill.to_field,
                         "customer_name": bill.customer_name, "truck_no": bill.truck_no, "invoice_no": bill.invoice_no, 'total': bill.total})
        data = json.dumps(data)
        return redirect(f'/export-csv/all-bills/?data={data}')
    return render(request, 'frontend/all-bills.html', {'bills': bills, "bill_count": bill_count, 'myFilter': myFilter})


'''
{"MVS LOGISTICS": [{"lr_no": "2332", "lr_date": "21/072023", "bill_no": "124", "bill_date": "24/072023", "from": "CHENNAI", "to": "KARUR", "total": 22000}], "M/S. CENTURY PLYBOARDS(INDIA) LIMITED": [{"lr_no": "2316,2317,2318", "lr_date": "04/072023", "bill_no": "108", "bill_date": "25/072023", "from": "CHENNAI", "to": "ARCOT,TIRUPATTUR,VELLORE", "total": 26400}, {"lr_no": "2312", "lr_date": "01/072023", "bill_no": "105", "bill_date": "27/072023", "from": "CHENNAI", "to": "CHIDAMBARAM", "total": 22000}, {"lr_no": "2307", "lr_date": "30/062023", "bill_no": "100", "bill_date": "25/072023", "from": "CHENNAI", "to": "DINDUGAL", "total": 35000}, {"lr_no": "2289,2290", "lr_date": "14/062023", "bill_no": "086", "bill_date": "25/072023", "from": "CHENNAI", "to": "DINDUGAL", "total": 34500}, {"lr_no": "2324", "lr_date": "09/072023", "bill_no": "117", "bill_date": "25/072023", "from": "CHENNAI", "to": "KALLAKURICHI", "total": 15000}, {"lr_no": "2301", "lr_date": "28/062023", "bill_no": "098", "bill_date": "25/072023", "from": "CHENNAI", "to": "KRISHNAGIRI", "total": 29400}, {"lr_no": "2310,2311", "lr_date": "01/072023", "bill_no": "104", "bill_date": "25/072023", "from": "CHENNAI", "to": "KRISHNAGIRI,HOSSUR", "total": 27500}, {"lr_no": "2329,2330", "lr_date": "17/072023", "bill_no": "122", "bill_date": "25/072023", "from": "CHENNAI", "to": "MADURAI", "total": 32200}, {"lr_no": "2296", "lr_date": "27/062023", "bill_no": "130", "bill_date": "27/072023", "from": "CHENNAI", "to": "MADURAI", "total": 30000}, {"lr_no": "2333", "lr_date": "21/072023", "bill_no": "129", "bill_date": "27/072023", "from": "CHENNAI", "to": "NAMAKKAL", "total": 22000}, {"lr_no": "2337", "lr_date": "26/072023", "bill_no": "128", "bill_date": "27/072023", "from": "CHENNAI", "to": "PERUNGALATHUR(DELIVERED AT PONDY)", "total": 11000}, {"lr_no": "2315", "lr_date": "03/072023", "bill_no": "107", "bill_date": "25/072023", "from": "CHENNAI", "to": "SALEM", "total": 24200}, {"lr_no": "2306", "lr_date": "30/062023", "bill_no": "099", "bill_date": "25/072023", "from": "CHENNAI", "to": "SALEM", "total": 24150}, {"lr_no": "2295", "lr_date": "24/062023", "bill_no": "095", "bill_date": "25/072023", "from": "CHENNAI", "to": "SALEM", "total": 22000}, {"lr_no": "2323", "lr_date": "08/072023", "bill_no": "114", "bill_date": "25/072023", "from": "CHENNAI", "to": "THIRUNULVELI", "total": 35000}, {"lr_no": "2313", "lr_date": "01/072023", "bill_no": "115", "bill_date": "27/072023", "from": "CHENNAI", "to": "VIRUDHACHALAM", "total": 23000}, {"lr_no": "2313", "lr_date": "01/072023", "bill_no": "110", "bill_date": "25/072023", "from": "CHENNAI", "to": "VIRUDHACHALAM(RETURN)", "total": 15000}, {"lr_no": "NIL", "lr_date": "05/072023", "bill_no": "120", "bill_date": "25/072023", "from": "MADHAVARAM", "to": "CHOOLAI", "total": 8500}]}
'''


def export_csv(request, req_type):
    dataset = request.GET.get('data')
    dataset = json.loads(dataset)
    response = HttpResponse(content_type='text/csv')
    filename = req_type.replace('-', ' ').capitalize()
    response['Content-Disposition'] = f'attachment; filename="{filename} {str(datetime.today()).split(".")[0]}.csv"'

    csv_writer = csv.writer(response, delimiter=',')
    if req_type == "statement":
        for c, group in dataset.items():
            print(c)
            csv_writer.writerow([c])
            csv_writer.writerow(["L.R. NO", "L.R. DATE", "BILL NO",
                                 "BILL DATE", "FROM", "TO", "TOTAL"])
            for r in group:
                print(r)
                csv_writer.writerow([r["lr_no"].replace(',', ';'), r["lr_date"], r["bill_no"],
                                     r["bill_date"], r["from"], r["to"], r["total"]])
    else:
        csv_writer.writerow(["L.R. NO", "L.R. DATE", "BILL NO",
                             "BILL DATE", "FROM", "TO", "CUSTOMER_NAME", "TRUCK_NO", "INVOICE_NO", "TOTAL"])
        for r in dataset:
            csv_writer.writerow([r["lr_no"].replace(',', ';'), r["lr_date"], r["bill_no"],
                                 r["bill_date"], r["from"], r["to"], r["customer_name"], r["truck_no"], r["invoice_no"].replace(',', ';'), r["total"]])

    return response
