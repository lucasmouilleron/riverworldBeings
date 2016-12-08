Riverworld Beings
=================

Characterisation of the population of beings of **Riverworld**.

Riverworld is a fictional planet and the setting for a series of sci-fi books written by **Philip José Farmer**.
Riverworld is an artificial environment where all humans (and pre-humans) ever born who died after reaching 5 years old are reconstructed.
Most of the resurrected awaken in a body equivalent to that of their 25 year old selves, in perfect health and free of any previous genetic or acquired defects.

A friend of mine made fun of the book concept and claimed half of the beings ressucitated would be prehistorical.

This project is proving him wrong.

Definitions
-----------
- Begining of mankind : Homo Erectus, 700K BC, assuming all beings on Riverworld can walk
- End of mankind : 2016. In the book, all people die in 1983 after interacting with an alien civilisation.
- Child Mortality *CM* : death of infants and children under the age of five
- Infant Mortality *IM* : death of infants and children under the age of one
- Life Expectancy *LE* : average time a being is expected to live
- Life Adult Expectancy *LAE* : average time a being is expected to live if he reachs 5 years old

Datas 
-----
- Dataset compiled amongst considered sources
- The dataset consists of Point In Times (*PIT*)
- For each *PIT*, these metrics are available : year, beings count in millions, *LE*, *LAE*, *CM* and continental proportions
- Depending on sources, *CM*, *IM*, *LE* and/or *LAE* are provided or not. Some datas have been extrapolated. Underlying model : *LE = CM * 5/2 + LAE * (1 - CM)*
- Case of beings count in prehistorical times : 
    - Beings counts estimation flucuates a lot. They can go as low as 1K individuals up to 100K
    - We have 3 milestones in our dataset : -700K (lower paleolithic), -50K (higher paleolithic) and -10K (begining of history)
    - For -10K, the poulation count is within the magnitude of the millions according to most of the sources. We kept the McEvedy estimation of 4 millions.
    - For -50K, we kept the higher estimation of Jean-Pierre Bocquet-Appel from his study of upper paleolithical meta populations. He found 30K individuals in the Aurignacien (-30K).
    - For -700K, we've assumed the population could not be higher than in -50K. We selected 10K individuals as 1K seemed very scary :-) 
- Case of *LE* et *CM* for prehistorical times :
    - As for beings counts, the *LE* estimations vary greatly
    - The Kaplan study suggest hunter gatherer modern societies tell us how prehistoric men lived and died. The study suggests the *ALE* is around 50 years and the *CM* around 0.5
    - For reference, the *CM* of 1900 is 0.4 and the Scheidel estimation of Classic Rome *CM* is 0.5
    - We cowardly derived the *CM* of pre Roman times to 0.6

Calculus
--------
- Linearity in between *PIT*s :
    - The underlying assumption is that the *PIT* metrics evolve linearly in between two *PIT*s
    - This assumption can be considered true from -700K to 1700, from 1700 to 1900, from 1900 to 1950 and from 1950 to today
    - The *PIT* resolution in the dataset is consistent with this observation
    - We then assume numerical midpoint integration is a reasonable estimation 
- For the period *PIT 1* => *PIT 2* 
- *AB yx = Amount of Beings for year x*
- Elapsed Time *ET = y2 - y1*
- Average Amount of Beings for Period *AABP = (AB y2 + AB y1) / 2*
- LAE for Period *LAEP = (LAE y1 + LAE y2) / 2*
- Proportion of Adult Beings for Period *PABP = 1 - ((CM y1 + CM y2) / 2)*
- Thus Amount of Beings who were Born for Period *ABP = ET * AABP / LAEP*
- Thus Amount of Adult Beings who were Born for Period *AABP = ET * AABP * PABP / LEP*
- Another calculus method is to use a simpe model of population growth :
    - *AB y1 = Ce^(r * y1)* and *AB y2 = Ce^(r * y2)* 
    - By integration, *ABP = ET * (AB y2 - AB y1) / (ln(AB y2) - ln(AB y1)) / LEP*

Results
-------
- Check the report : ./output/report.pdf
- Check the plots : ./output

Sources
-------
- [https://en.wikipedia.org/wiki/Human_evolution](https://en.wikipedia.org/wiki/Human_evolution)
- [https://ourworldindata.org/child-mortality](https://ourworldindata.org/child-mortality)
- [https://ourworldindata.org/infant-mortality](https://ourworldindata.org/infant-mortality)
- [https://en.wikipedia.org/wiki/Life_expectancy#Variation_over_time](https://en.wikipedia.org/wiki/Life_expectancy#Variation_over_time)
- [https://en.wikipedia.org/wiki/World_population#Past_population](https://en.wikipedia.org/wiki/World_population#Past_population)
- [https://ourworldindata.org/world-population-growth](https://ourworldindata.org/world-population-growth)
- [http://www.unm.edu/~hkaplan/KaplanHillLancasterHurtado_2000_LHEvolution.pdf](http://www.unm.edu/~hkaplan/KaplanHillLancasterHurtado_2000_LHEvolution.pdf)
- [https://en.wikipedia.org/wiki/Prehistoric_demography](https://en.wikipedia.org/wiki/Prehistoric_demography)
- [https://en.wikipedia.org/wiki/World_population_estimates](https://en.wikipedia.org/wiki/World_population_estimates)
- [http://www.evolhum.cnrs.fr/bocquet/jas2005.pdf](http://www.evolhum.cnrs.fr/bocquet/jas2005.pdf)
- [https://www.princeton.edu/~pswpc/pdfs/scheidel/040901.pdf](https://www.princeton.edu/~pswpc/pdfs/scheidel/040901.pdf)
- [https://scholarspace.manoa.hawaii.edu/bitstream/handle/10125/17288/AP-v47n2-190-209.pdf](https://scholarspace.manoa.hawaii.edu/bitstream/handle/10125/17288/AP-v47n2-190-209.pdf)
- [https://ourworldindata.org/world-population-growth](https://ourworldindata.org/world-population-growth)
- [http://www.math.hawaii.edu/~ramsey/People.html](http://www.math.hawaii.edu/~ramsey/People.html)

Install
-------
- `pip install --upgrade pip`
- `pip install -r requirements.txt --user`
- Fonts used in this project : `./resources/fonts`
- PDF dependencies : 
    - mac : `brew cask install wkhtmltopdf`
    - linux : `apt-get install wkhtmltopdf`

Run
---
- Configuration is loaded from `config.ini`
- `python riverworld.py`

Credits
-------
- Author : Lucas Mouilleron, [http://lucasmouilleron.com](http://lucasmouilleron.com)
- Thanks to : Jean-Benoît Bourron, Romain Charlassier
---


Results
=======


Main results
------------

| metric                                                  | value         |
|:--------------------------------------------------------|:--------------|
| total beigns ever born                                  | 60.3 billions |
| total adult beigns ever born                            | 17.2 billions |
| proportion of alive beings amongst all beings ever born | 9.4%          |
| median year of adult beings ever born                   | 1000          |
| median year of beings ever born                         | 0             |{: .std-table }


Proportion of adult beings amongst all adults ever born
-------------------------------------------------------

| sub population                                         | value              |
|:-------------------------------------------------------|:-------------------|
| me                                                     | 1.65806845229e-09% |
| Asians                                                 | 52%                |
| Paloelithical era                                      | 1.0%               |
| Neolithical era                                        | 7.3%               |
| -10K until the birh of Jesus Christ                    | 22.0%              |
| Classical Athens (508 BC - 322 BC) (with civil rights) | 0.001%             |
| Classical Athens (508 BC - 322 BC)                     | 0.007%             |
| Roman Republic (509 BC - 27 BC)                        | 0.02%              |
| Western Roman Empire (27 BC - 476 AD)                  | 3.4%               |
| after WWII                                             | 30%                |{: .std-table }

---


Adult beings results
--------------------

![image](/Users/lucas/Projects%20Software/haveidols/riverworldBeings/libs/../output/Riverworld_Distribution_Of_Adult_Beings_Eras_Amongst_All_Adult_Beings_Ever_Born.png){: .plot }

figure 1
{: .legend }

![image](/Users/lucas/Projects%20Software/haveidols/riverworldBeings/libs/../output/Riverworld_Distribution_Of_Adult_Beings_Continents_Amongst_All_Adult_Beings_Ever_Born.png){: .plot }

figure 2
{: .legend }

![image](/Users/lucas/Projects%20Software/haveidols/riverworldBeings/libs/../output/Riverworld_Cumulated_Amount_Of_Adult_Beings_Ever_Born.png){: .plot }

figure 3
{: .legend }

---


All beings results
------------------

![image](/Users/lucas/Projects%20Software/haveidols/riverworldBeings/libs/../output/Riverworld_Distribution_Of_Beings_Eras_Amongst_All_Beings_Ever_Born.png){: .plot }

figure 4
{: .legend }

![image](/Users/lucas/Projects%20Software/haveidols/riverworldBeings/libs/../output/Riverworld_Cumulated_Amount_Of_Beings_Ever_Born.png){: .plot }

figure 5
{: .legend }

![image](/Users/lucas/Projects%20Software/haveidols/riverworldBeings/libs/../output/Riverworld_Cumulated_Amount_Of_Beings_Ever_Born_-_Calculs_Comparaison.png){: .plot }

figure 6
{: .legend }

