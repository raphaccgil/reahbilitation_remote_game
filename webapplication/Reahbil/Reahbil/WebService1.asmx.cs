using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Services;

namespace Reahbil
{
    /// <summary>
    /// Summary description for WebService1
    /// </summary>
    [WebService(Namespace = "http://tempuri.org/")]
    [WebServiceBinding(ConformsTo = WsiProfiles.BasicProfile1_1)]
    [System.ComponentModel.ToolboxItem(false)]
    // To allow this Web Service to be called from script, using ASP.NET AJAX, uncomment the following line. 
    // [System.Web.Script.Services.ScriptService]
    public class WebService1 : System.Web.Services.WebService
    {

        [WebMethod]
        public string HelloWorld()
        {
            return "Hello man";
        }
        [WebMethod]
        public decimal Hello(decimal valorC, decimal valorD)
        {
            decimal alfa = 0;
            if (valorC > 3)
                {
                return alfa = decimal.Divide(valorC, valorD);
                } 
            else 
                {
                return alfa = decimal.Add(valorC, valorD);
                }
        }

        [WebMethod]
        public decimal Calculadora(decimal ValorA, decimal ValorB, OperacoesBasicas TipoOperacao)
        {
            decimal ResultadoAB = 0;

            switch (TipoOperacao)
            {
                case OperacoesBasicas.Adicao:
                    {
                        ResultadoAB = decimal.Add(ValorA, ValorB);
                        break;
                    }
                case OperacoesBasicas.Divisao:
                    {
                        ResultadoAB = decimal.Divide(ValorA, ValorB);
                        break;
                    }
                case OperacoesBasicas.Multiplicacao:
                    {
                        ResultadoAB = decimal.Multiply(ValorA, ValorB);
                        break;
                    }
                case OperacoesBasicas.Subtracao:
                    {
                        ResultadoAB = decimal.Subtract(ValorA, ValorB);
                        break;
                    }
            }

            return ResultadoAB;
        }
        public enum OperacoesBasicas
{
	Adicao = 0,
	Divisao = 1,
	Multiplicacao = 2,
	Subtracao = 3
}
    }
}
