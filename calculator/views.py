from django.shortcuts import render
from django.views import View
from .forms import InvestmentForm


# Create your views here.
class Index(View):
    def get(self, request):
        form = InvestmentForm()
        return render(request, 'calculator/index.html', {'form': form})

    def post(self, request):
        form = InvestmentForm(request.POST)

        if form.is_valid():
            total_result = form.cleaned_data['starting_amount']
            total_interest = 0 # juros totais
            yearly_results = {} # resultados anuais

            for i in range(1, int(form.cleaned_data['number_of_years'] + 1)):
                yearly_results[i] = {}

                #  Calcular os juros
                interest = total_result * (form.cleaned_data['return_date'] / 100)
                total_result += interest
                total_interest += interest
                
                #  Adicionar contribuição adicional
                total_result += form.cleaned_data['annual_additional_contribution']


                # Definir resultados anuais
                yearly_results[i]['interest'] = round(total_interest, 2)
                yearly_results[i]['total'] = round(total_result, 2)

                # Criar o contexto
                context = {
                    'total_results': round(total_result, 2),
                    'yearly_results': yearly_results,
                    'number_of_years': int(form.cleaned_data['number_of_years']),
                }

            # Retornar o template
            return render(request, 'calculator/result.html', context)

