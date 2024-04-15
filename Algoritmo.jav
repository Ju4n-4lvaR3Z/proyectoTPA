import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

/* ----------------------------------------------------------------------
 * Esta clase implementa con memoria dinámica los arboles binarios. 
 * La idea es que un árbol binario tiene una raiz y un hijo izquierdo
 * y un hijo derecho que son a su vez árboles binarios
 * El parámetro elemento representa la clase de los elementos del arbol
 * -----------------------------------------------------------------------*/
 
class ArbolBinario<Elemento> implements Cloneable{
   
   private ArrayList<Elemento> volcado, hojas, cola, colaAux;
   private ArrayList<Integer> grado;
   //Almacena la raiz del arbol    
   private Elemento raiz;
   // enlazan con lis hijos izquierdo y derecho 
   private ArbolBinario<Elemento> hi,hd, aux;
   
   //CONSTRUCTORES
    
   //Crea un arbol vacio. Un arbol vacio no apunta a null.
   //Apunta a un arbol con todos sus atributos a null 
   public ArbolBinario(){
   
      raiz=null;
      hi=hd=aux=null;
      volcado = new ArrayList<Elemento>();
      hojas = new ArrayList<Elemento>();
      grado = new ArrayList<Integer>();
      cola = new ArrayList<Elemento>();
      colaAux = new ArrayList<Elemento>();
      
   }
   
   //Crea un arbol con solo la raiz si esta no es null. Si es null se crea un 
   //arbol vacio los hijos son ambos arboles vacios. 
   public ArbolBinario(Elemento ob){
      this();
      raiz=ob;
      if (raiz!=null) hi=hd=new ArbolBinario<Elemento>();
   }
   
   public void construir(ArbolBinario<Elemento> izqdo,Elemento r,ArbolBinario<Elemento> derecho){
      //Si la raiz es null se crea un arbol vacio. 	
      if (r==null){
         raiz=null;
         hd=hi=null;
      }else{
         raiz=r;
         //Si algun hijo es null se pondri un arbol vacio
         if (izqdo==null) hi=new ArbolBinario<Elemento>();
         else hi=izqdo;
         if (derecho==null) hd=new ArbolBinario<Elemento>();
         else hd=derecho;
      }
    }
     
    // Construye un arbol con solo la raiz y las consideraciones anteriores 	
    public void construir(Elemento ob){
      construir(new ArbolBinario<Elemento>(),ob,new ArbolBinario<Elemento>());
    }
    
    // Construye un arbol vacio 
    public void construir(){
        raiz=null;
        hi=hd=null;
    }
    
    // Devuelve la raiz o null si es vacio 
    public Elemento raiz(){ return raiz; }
    
    // Devuelve el hijo izquierdo o null si es vacio 
    public ArbolBinario<Elemento> hi(){ return hi; }
    
    // Devuelve el hijo derecho o null si es vacio 
    public ArbolBinario<Elemento> hd(){ return hd; }
    
    // Decide si el arbol esta vacio; falso en caso contrario 
    public boolean esVacio(){ return  raiz==null; }

    //OTRAS OPERACIONES
    
    // Muestra el arbol  
    @Override public String toString(){ return "\n"+toString(0); }    
    
    // Muestra el arbol con una sangr�a de espacios
    // y un recorrido "raiz-izquierda-derecha" */
    public String toString(int espacios){
       String linea="";
       for (int x=0;x<=espacios;x++) linea=linea+" ";
       
       if (esVacio()) linea=linea+"vacio"+this.getClass();
       else{
          linea=linea+raiz().toString()+this.getClass();
	  if (!esHoja()){
	     linea=linea+"\n  "+hi().toString(espacios+2);
	     linea=linea+"\n  "+hd().toString(espacios+2);
	  }  
       }
       return linea;
    }
    
    // True si es hoja, false si no lo es  
    public boolean esHoja(){
	return  !esVacio() && hi().esVacio() && hd().esVacio() ;
    }
    
    // True si dos �rboles son iguales, false en caso contrario  */
    @Override  public boolean equals(Object arbol){
       boolean igual=false;
       if (arbol instanceof ArbolBinario){
            ArbolBinario<Elemento> a=(ArbolBinario<Elemento>) arbol;
            igual= a==this || (esVacio() && a.esVacio());
            if (!igual)
               	if ((!esVacio() && a.esVacio())||(esVacio()&& !a.esVacio())) igual=false;
		else//ninguno es vacio
                   igual=a.raiz().equals(raiz())&&a.hi().equals(hi())&&a.hd().equals(hd());
       }
       return igual;
    }     
    
    // Devuelve la altura: longitud de la rama mas larga  */
    public int altura()throws Exception{
       int i=0;
       if (!esVacio())
         i=Math.max(hd().altura(),hi().altura())+1;
       return i;
    }
    
    // Devuelve la prundidad: longitud desde la raiz hasta el elemento parámetro
    // es el nivel. La raiz tiene nivel 0  
    public int profundidad(Elemento a){
        int prof=-1;
        if (!esVacio()){
            if (raiz().equals(a)) prof=0;
            else {
                  prof=hi().profundidad(a);
                  if (prof!=-1)  prof++;
                  else {
                      prof=hd().profundidad(a);
                      if (prof!=-1)  prof++;
                  }
            }
        }
        return prof;
    }
    // Devuelve la prundidad: longitud desde la raiz hasta el árbol parámetro
    // es el nivel. La raiz tiene nivel 0  
    public int profundidad(ArbolBinario<Elemento> a){
        int prof=-1;
        if (!esVacio()){
            if (this.equals(a)) prof=0;
            else {
                  prof=hi().profundidad(a);
                  if (prof!=-1)  prof++;
                  else {
                      prof=hd().profundidad(a);
                      if (prof!=-1)  prof++;
                  }
            }
        }
        return prof;
    }
    
    // Devuelve el primer árbol, con un recorrido "raiz-izquierda-derecha",
    // que tiene por raiz el elemento parámetro
    // Si no lo encuentra devuelve un arbol vacio  */
    public ArbolBinario<Elemento> localiza(Elemento ob){
	ArbolBinario<Elemento> aux=new ArbolBinario<Elemento>();
	if (!esVacio()){
            if (raiz().equals(ob)) aux=this;
            else{
		aux=hi().localiza(ob);
		if (aux.esVacio())//no lo encuentra en hi
                    aux=hd().localiza(ob);
		}
	}
	return aux;
    }
    
    // True si el elemento pertenec, false en caso contrario  
    public boolean pertenece(Elemento e){
        return !localiza(e).esVacio();
    }
    
    //Devuelve el primer arbol, con un recorrido "raiz-izquierda-derecha",
    // que tiene por hijo el elemento parametro
    // Si no lo encuentra devuelve un arbol vacio  
    public ArbolBinario<Elemento> padre(Elemento ob){
       ArbolBinario<Elemento> aux=new ArbolBinario<Elemento>();
       if (!esVacio()){
            if ( ( (!hi().esVacio()) && (ob.equals(hi().raiz())) )
               ||( (!hd().esVacio()) && (ob.equals(hd().raiz())) ) )
               	aux=this;
            else{
		aux=hi().padre(ob);
		if ( aux.esVacio() )  aux=hd().padre(ob);
            }
        }
        return aux;
    }
    
    // No se pueden eliminar elementos  		
    public void eliminar(Elemento dato)throws Exception{
	//sobre escribimos en arbol binario ordenado
    }                          
    
    //Devuelve una copia  
    @Override public ArbolBinario<Elemento> clone()throws CloneNotSupportedException{
    
       ArbolBinario<Elemento> copia=new ArbolBinario<Elemento>();
       try{
          if(!esVacio()) copia.construir(hi().clone(),raiz(),hd().clone());
       } catch(CloneNotSupportedException e){
          copia=new ArbolBinario<Elemento>();
       }
       return copia;
    }
    
/* Función recursiva llamada "AtraviesaInOrden" que se encarga de ir atravezando por 'In-Orden' 
   el árbol y ademas va imprimiendolo en 'In-Orden' */

public void AtraviesaInOrden(ArbolBinario<Elemento> a){
   if(esVacio()) 
       System.out.println("EL ARBOL ESTA VACIO");
   else{
       if(a.raiz()!=null){
          //System.out.println("Entre IFIF");// Condición de termino de la recursividad, en este caso es cuendo el puntero que apuntado 0
          AtraviesaInOrden(a.hi());      // Recorre hasta el ultimo hijo izquierdo
          System.out.print(" "+a.raiz().toString()+" ");        // Imprime en pantalla en In-Orden
          AtraviesaInOrden(a.hd());            // Luego va por el hijo derecho de la posición respectiva
       }
   }
}

/* Función recursiva llamada "AtraviesaPostOrden" que se encarga de ir atravezando por 'Post-Orden' 
   el árbol y ademas va imprimiendolo en 'Post-Orden' */

public void AtraviesaPostOrden(ArbolBinario<Elemento> a){   
    if(esVacio()) 
       System.out.println("EL ARBOL ESTA VACIO");
   else{
       if(a.raiz()!=null){       // Condición de termino de la recursividad, en este caso es cuendo el puntero que apuntado 0
          AtraviesaPostOrden(a.hi());   // Recorre hasta el ultimo hijo izquierdo
          AtraviesaPostOrden(a.hd());         // Luego va por el hijo derecho de la posición respectiva
          System.out.print(" "+a.raiz().toString()+" ");             // Imprime en pantalla en Post-Orden
       }
   }
}

/* Función recursiva llamada "AtraviesaPreOrden" que se encarga de ir atravezando por 'Pre-Orden' 
   el árbol y ademas va imprimiendolo en 'Pre-Orden' */

public void AtraviesaPreOrden(ArbolBinario<Elemento> a){
    if(esVacio()) 
       System.out.println("EL ARBOL ESTA VACIO");
   else{
       if(a.raiz()!=null){       // Condición de termino de la recursividad, en este caso es cuendo el puntero que apuntado 0
          System.out.print(" "+a.raiz().toString()+" "); // Imprime en pantalla en Post-Orden
          AtraviesaPreOrden(a.hi());            // Recorre hasta el ultimo hijo izquierdo
          AtraviesaPreOrden(a.hd());            // Luego va por el hijo derecho de la posición respectiva
        }
   }
}

public boolean ComparaArboles(ArbolBinario<Elemento> a, ArbolBinario<Elemento> b){
    if(a.esVacio() && b.esVacio())
        return true;
    else if(a.esVacio() || b.esVacio())
        return false;
    else{
        return (FuncionCompara(a.raiz(),b.raiz()) &&
                ComparaArboles(a.hd(),b.hd()) &&
                ComparaArboles(a.hi(),b.hi())
                );
    }
}

public boolean FuncionCompara (Elemento a, Elemento b){
        if(a.equals(b))
            return true;
        else return false;
}

public void Volcar(ArbolBinario<Elemento> a){
   if(esVacio()) 
       System.out.println("EL ARBOL ESTA VACIO");
   else{
       if(a.raiz()!=null){
          //System.out.println("Entre IFIF");// Condición de termino de la recursividad, en este caso es cuendo el puntero que apuntado 0
          Volcar(a.hi());      // Recorre hasta el ultimo hijo izquierdo
          volcado.add(a.raiz());
          Volcar(a.hd());            // Luego va por el hijo derecho de la posición respectiva
       }
   }
}
public void ImprimirVolcado(){
        System.out.print(" "+volcado.toString()+" ");
}

public void CantHojas(ArbolBinario<Elemento> a){
   if(esVacio()) 
       System.out.println("EL ARBOL ESTA VACIO");
   else{
       if(a.raiz()!=null){       // Condición de termino de la recursividad, en este caso es cuendo el puntero que apuntado 0
          CantHojas(a.hi());   // Recorre hasta el ultimo hijo izquierdo
          CantHojas(a.hd());         // Luego va por el hijo derecho de la posición respectiva
          if(a.esHoja())
              hojas.add(a.raiz());
       }
   }
}

public void ImprimirCantHojas(){
        System.out.println("La Cantidad de Hojas del Arbol es "+hojas.size());
}


public void GradoArbol(ArbolBinario<Elemento> a){
    int x=0;
   if(esVacio()) 
       System.out.println("EL ARBOL ESTA VACIO");
   else{
       //System.out.println("La raiz es: "+a.raiz);
       if(!a.esVacio()){       // Condición de termino de la recursividad, en este caso es cuendo el puntero que apuntado 0
         
           if(!a.hi().esVacio()){
               x++;
               //System.out.println("Entrehi"+x);
           }
           if(!a.hd().esVacio()){
               x++;
               //System.out.println("EntreHD"+x);
           }
           //System.out.println("Agrego "+x);
           grado.add(x);
           
           GradoArbol(a.hi());   // Recorre hasta el ultimo hijo izquierdo
           GradoArbol(a.hd());         // Luego va por el hijo derecho de la posición respectiva
           
       }
   }
}

public void MayorArreglo(){
    int x=0, aux=0, largo=grado.size();
    for(int i=0;i<largo;i++){
        if(x<grado.get(i)){
            x=grado.get(i);
                       //System.out.println("XEs"+x);

        }
    }
    System.out.println("El Grado Es: "+x);
}

public void verCompleto(){
    int x=2, flag=1, largo=grado.size();
    for(int i=0;i<largo;i++){
        //System.out.println("Vector "+grado.get(i));
        if(x!=grado.get(i)&&grado.get(i)>0){
            flag=0;
        }
    }
    if(flag==1){
        System.out.println("El Arbol es Completo ");
    }
    else System.out.println("El Arbol NO es Completo ");
    
}

//Hijos de un determinado Nivel
public void imprimirEntreConNivel (ArbolBinario<Elemento>  a, int nivel, int actual)  {
        if (!a.esVacio()) {  
            if(nivel==actual){
                System.out.print(" "+a.raiz().toString()+" (Nivel "+actual+") - ");
            }
            imprimirEntreConNivel (a.hi(),nivel,actual+1);
            imprimirEntreConNivel (a.hd(),nivel,actual+1);
        }
}

//NO se esta usando
public void anchuraArbol (ArbolBinario<Elemento>  a, int nivel)  {
        if (!a.esVacio()) {
            System.out.print(" "+a.raiz().toString()+" (Nivel "+nivel+") - ");
            anchuraArbol (a.hi(),nivel+1);
            anchuraArbol (a.hd(),nivel+1);
            
        }
}
}