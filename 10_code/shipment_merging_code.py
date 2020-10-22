{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from plotnine import *\n",
    "\n",
    "%load_ext lab_black"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "data = pd.read_csv(\n",
    "    \"https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioids-2020-purlple-team/TommyTseng/20_intermediate_files/2006-2012_prescription_10States.csv?token=ARFW6V4S5VDU67LL2NAFKES7S4I7Y\"\n",
    ")\n",
    "pop = pd.read_csv(\n",
    "    \"https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioids-2020-purlple-team/ssloate/20_intermediate_files/countypopulations_clean.csv?token=ARFW6VYROFILNMBNR2ENMEK7SXUKK\"\n",
    ")\n",
    "fips = pd.read_excel(\n",
    "    \"/Users/samsloate/Desktop/Data_Science/Opioids_Project/estimating-impact-of-opioids-2020-purlple-team/00_source/fips_codes.xlsx\"\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "data = data.copy()\n",
    "pop = pop.copy()\n",
    "fips = fips.copy()\n",
    "data = data.rename(\n",
    "    columns={\"BUYER_STATE\": \"State\", \"BUYER_COUNTY\": \"County\", \"YEAR\": \"Year\"}\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# change County columns to sentence case and add the word county at the end\n",
    "data[\"County\"] = data[\"County\"].str.capitalize()\n",
    "\n",
    "# add County to end\n",
    "data[\"County\"] = data[\"County\"] = data[\"County\"] + \" County\"\n",
    "\n",
    "# change fips column name to match County\n",
    "fips = fips.rename(columns={\"Full Name\": \"County\"})\n",
    "\n",
    "# drop _merge column in pop\n",
    "pop = pop.drop(columns=\"_merge\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# drop Alaska (Nick said to) and Louisiana (we know they aren't a match based on other graphing)\n",
    "data = data[data[\"State\"] != \"AK\"]\n",
    "data = data[data[\"State\"] != \"LA\"]\n",
    "fips = fips[fips[\"State\"] != \"AK\"]\n",
    "fips = fips[fips[\"State\"] != \"LA\"]\n",
    "\n",
    "\n",
    "# make new fips dataset for only the states we have in the shipment dataset\n",
    "fips_cut = fips.loc[fips[\"State\"].isin(list(data[\"State\"].unique()))]\n",
    "\n",
    "# check it's the right length / has all states\n",
    "assert len(fips_cut.State.unique()) == len(list(data[\"State\"].unique()))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "10"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(list(data[\"State\"].unique()))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# merge data\n",
    "merged = pd.merge(fips_cut, data, on=[\"County\", \"State\"], how=\"outer\", indicator=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>FIPS</th>\n",
       "      <th>County</th>\n",
       "      <th>State</th>\n",
       "      <th>State Name</th>\n",
       "      <th>Year</th>\n",
       "      <th>Total_Weight</th>\n",
       "      <th>_merge</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1156</th>\n",
       "      <td>13053</td>\n",
       "      <td>Chattahoochee County</td>\n",
       "      <td>GA</td>\n",
       "      <td>Georgia</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1318</th>\n",
       "      <td>13101</td>\n",
       "      <td>Echols County</td>\n",
       "      <td>GA</td>\n",
       "      <td>Georgia</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1784</th>\n",
       "      <td>13239</td>\n",
       "      <td>Quitman County</td>\n",
       "      <td>GA</td>\n",
       "      <td>Georgia</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1864</th>\n",
       "      <td>13265</td>\n",
       "      <td>Taliaferro County</td>\n",
       "      <td>GA</td>\n",
       "      <td>Georgia</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2005</th>\n",
       "      <td>13307</td>\n",
       "      <td>Webster County</td>\n",
       "      <td>GA</td>\n",
       "      <td>Georgia</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3744</th>\n",
       "      <td>26083</td>\n",
       "      <td>Keweenaw County</td>\n",
       "      <td>MI</td>\n",
       "      <td>Michigan</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4221</th>\n",
       "      <td>28055</td>\n",
       "      <td>Issaquena County</td>\n",
       "      <td>MS</td>\n",
       "      <td>Mississippi</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4768</th>\n",
       "      <td>37029</td>\n",
       "      <td>Camden County</td>\n",
       "      <td>NC</td>\n",
       "      <td>North Carolina</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4993</th>\n",
       "      <td>37095</td>\n",
       "      <td>Hyde County</td>\n",
       "      <td>NC</td>\n",
       "      <td>North Carolina</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>left_only</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       FIPS                County State      State Name  Year  Total_Weight  \\\n",
       "1156  13053  Chattahoochee County    GA         Georgia   NaN           NaN   \n",
       "1318  13101         Echols County    GA         Georgia   NaN           NaN   \n",
       "1784  13239        Quitman County    GA         Georgia   NaN           NaN   \n",
       "1864  13265     Taliaferro County    GA         Georgia   NaN           NaN   \n",
       "2005  13307        Webster County    GA         Georgia   NaN           NaN   \n",
       "3744  26083       Keweenaw County    MI        Michigan   NaN           NaN   \n",
       "4221  28055      Issaquena County    MS     Mississippi   NaN           NaN   \n",
       "4768  37029         Camden County    NC  North Carolina   NaN           NaN   \n",
       "4993  37095           Hyde County    NC  North Carolina   NaN           NaN   \n",
       "\n",
       "         _merge  \n",
       "1156  left_only  \n",
       "1318  left_only  \n",
       "1784  left_only  \n",
       "1864  left_only  \n",
       "2005  left_only  \n",
       "3744  left_only  \n",
       "4221  left_only  \n",
       "4768  left_only  \n",
       "4993  left_only  "
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# fix inaccuracies\n",
    "\n",
    "data[\"County\"].replace(\"De kalb County\", \"De Kalb County\", inplace=True)\n",
    "data[\"County\"].replace(\"Dekalb County\", \"De Kalb County\", inplace=True)\n",
    "data[\"County\"].replace(\"Saint clair County\", \"St. Clair County\", inplace=True)\n",
    "data[\"County\"].replace(\"Hot spring County\", \"Hot Spring County\", inplace=True)\n",
    "data[\"County\"].replace(\"Little river County\", \"Little River County\", inplace=True)\n",
    "data[\"County\"].replace(\"Saint francis County\", \"St. Francis County\", inplace=True)\n",
    "data[\"County\"].replace(\"Van buren County\", \"Van Buren County\", inplace=True)\n",
    "data[\"County\"].replace(\"Desoto County\", \"De Soto County\", inplace=True)\n",
    "data[\"County\"].replace(\"De soto County\", \"De Soto County\", inplace=True)\n",
    "data[\"County\"].replace(\"Indian river County\", \"Indian River County\", inplace=True)\n",
    "data[\"County\"].replace(\"Miami-dade County\", \"Miami-Dade County\", inplace=True)\n",
    "data[\"County\"].replace(\"Palm beach County\", \"Palm Beach County\", inplace=True)\n",
    "data[\"County\"].replace(\"Saint johns County\", \"St. Johns County\", inplace=True)\n",
    "data[\"County\"].replace(\"Saint lucie County\", \"St. Lucie County\", inplace=True)\n",
    "data[\"County\"].replace(\"Santa rosa County\", \"Santa Rosa County\", inplace=True)\n",
    "data[\"County\"].replace(\"Ben hill County\", \"Ben Hill County\", inplace=True)\n",
    "data[\"County\"].replace(\"Jeff davis County\", \"Jeff Davis County\", inplace=True)\n",
    "data[\"County\"].replace(\"Pearl river County\", \"Pearl River County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mcdowell County\", \"McDowell County\", inplace=True)\n",
    "data[\"County\"].replace(\"New hanover County\", \"New Hanover County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mccormick County\", \"McCormick County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mcduffie County\", \"McDuffie County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mcintosh County\", \"McIntosh County\", inplace=True)\n",
    "data[\"County\"].replace(\"Jefferson davis County\", \"Jefferson Davis County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mcnairy County\", \"McNairy County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mcminn County\", \"McMinn County\", inplace=True)\n",
    "data[\"County\"].replace(\"Saint joseph County\", \"St. Joseph County\", inplace=True)\n",
    "data[\"County\"].replace(\"Presque isle County\", \"Presque Isle County\", inplace=True)\n",
    "data[\"County\"].replace(\"Grand traverse County\", \"Grand Traverse County\", inplace=True)\n",
    "data[\"County\"].replace(\"Rock island County\", \"Rock Island County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mclean County\", \"McLean County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mchenry County\", \"McHenry County\", inplace=True)\n",
    "data[\"County\"].replace(\"Mcdonough County\", \"McDonough County\", inplace=True)\n",
    "data[\"County\"].replace(\"La salle County\", \"LaSalle County\", inplace=True)\n",
    "data[\"County\"].replace(\"Jo daviess County\", \"Jo Daviess County\", inplace=True)\n",
    "data[\"County\"].replace(\"Dupage County\", \"Du Page County\", inplace=True)\n",
    "data[\"County\"].replace(\"Dewitt County\", \"De Witt County\", inplace=True)\n",
    "data[\"County\"].replace(\"Black hawk County\", \"Black Hawk County\", inplace=True)\n",
    "data[\"County\"].replace(\"Buena vista County\", \"Buena Vista County\", inplace=True)\n",
    "data[\"County\"].replace(\"Cerro gordo County\", \"Cerro Gordo County\", inplace=True)\n",
    "data[\"County\"].replace(\"Des moines County\", \"Des Moines County\", inplace=True)\n",
    "data[\"County\"].replace(\"Obrien County\", \"O Brien County\", inplace=True)\n",
    "data[\"County\"].replace(\"Palo alto County\", \"Palo Alto County\", inplace=True)\n",
    "\n",
    "merged = pd.merge(fips_cut, data, on=[\"County\", \"State\"], how=\"outer\", indicator=True)\n",
    "merged[merged[\"_merge\"] != \"both\"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['Quitman County', 'Webster County', 'Echols County', 'Taliaferro County', 'Chattahoochee County']\n",
      "['Issaquena County']\n",
      "['Hyde County', 'Camden County']\n"
     ]
    }
   ],
   "source": [
    "# check that there's no weird misspellings of the counties or other obvious misaignments\n",
    "ga_fips = list(fips[fips[\"State\"].isin([\"GA\"])][\"County\"].unique())\n",
    "ga_data = list(data[data[\"State\"].isin([\"GA\"])][\"County\"].unique())\n",
    "print(list(set(ga_fips) - set(ga_data)))\n",
    "\n",
    "ms_fips = list(fips[fips[\"State\"].isin([\"MS\"])][\"County\"].unique())\n",
    "ms_data = list(data[data[\"State\"].isin([\"MS\"])][\"County\"].unique())\n",
    "print(list(set(ms_fips) - set(ms_data)))\n",
    "\n",
    "nc_fips = list(fips[fips[\"State\"].isin([\"NC\"])][\"County\"].unique())\n",
    "nc_data = list(data[data[\"State\"].isin([\"NC\"])][\"County\"].unique())\n",
    "print(list(set(nc_fips) - set(nc_data)))\n",
    "\n",
    "# the remaining counties are not in the original dataset, likely because they had no drug shipments. We are okay omitting these."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>State</th>\n",
       "      <th>State Name</th>\n",
       "      <th>County</th>\n",
       "      <th>FIPS</th>\n",
       "      <th>Year</th>\n",
       "      <th>Total_Weight</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>AR</td>\n",
       "      <td>Arkansas</td>\n",
       "      <td>Arkansas County</td>\n",
       "      <td>5001</td>\n",
       "      <td>2006.0</td>\n",
       "      <td>4830.744670</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>AR</td>\n",
       "      <td>Arkansas</td>\n",
       "      <td>Arkansas County</td>\n",
       "      <td>5001</td>\n",
       "      <td>2007.0</td>\n",
       "      <td>5950.277375</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>AR</td>\n",
       "      <td>Arkansas</td>\n",
       "      <td>Arkansas County</td>\n",
       "      <td>5001</td>\n",
       "      <td>2008.0</td>\n",
       "      <td>6418.230308</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>AR</td>\n",
       "      <td>Arkansas</td>\n",
       "      <td>Arkansas County</td>\n",
       "      <td>5001</td>\n",
       "      <td>2009.0</td>\n",
       "      <td>6643.993313</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>AR</td>\n",
       "      <td>Arkansas</td>\n",
       "      <td>Arkansas County</td>\n",
       "      <td>5001</td>\n",
       "      <td>2010.0</td>\n",
       "      <td>7564.533495</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  State State Name           County  FIPS    Year  Total_Weight\n",
       "0    AR   Arkansas  Arkansas County  5001  2006.0   4830.744670\n",
       "1    AR   Arkansas  Arkansas County  5001  2007.0   5950.277375\n",
       "2    AR   Arkansas  Arkansas County  5001  2008.0   6418.230308\n",
       "3    AR   Arkansas  Arkansas County  5001  2009.0   6643.993313\n",
       "4    AR   Arkansas  Arkansas County  5001  2010.0   7564.533495"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# make final FIPS/drug shipment dataset\n",
    "drugship = merged[merged[\"_merge\"] == \"both\"]\n",
    "\n",
    "assert (drugship._merge == \"both\").all()\n",
    "\n",
    "# drop _merge column and reorder\n",
    "drugship = drugship.drop(columns=\"_merge\")\n",
    "drugship = drugship[[\"State\", \"State Name\", \"County\", \"FIPS\", \"Year\", \"Total_Weight\"]]\n",
    "drugship.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "# merge in population data. Use left because not all states are in dataset; want to keep all drugship observations\n",
    "\n",
    "drug_pop = pd.merge(\n",
    "    drugship, pop, on=[\"FIPS\", \"Year\"], how=\"left\", validate=\"m:m\", indicator=True\n",
    ")\n",
    "# check\n",
    "assert (drug_pop._merge == \"both\").all()\n",
    "\n",
    "# drop irrelevant columns\n",
    "drug_pop = drug_pop.drop(\n",
    "    columns=[\"County_x\", \"State Name_x\", \"Unnamed: 0\", \"State\", \"_merge\"]\n",
    ")\n",
    "# rename colums\n",
    "drug_pop = drug_pop.rename(columns={\"State Name_y\": \"State\", \"County_y\": \"County\"})\n",
    "\n",
    "# reorder columns\n",
    "drug_pop = drug_pop[\n",
    "    [\"State Abbr\", \"State\", \"County\", \"FIPS\", \"Year\", \"Total_Weight\", \"Population\"]\n",
    "]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "# do some reasonableness checks\n",
    "assert len(drug_pop[\"State\"].unique()) == len(list(data[\"State\"].unique()))\n",
    "assert (drug_pop[\"Total_Weight\"] > 0).all\n",
    "assert (drug_pop[\"Population\"] > 0).all"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create drug shipment per capita column\n",
    "# Create per capita deaths column\n",
    "drug_pop[\"PerCapWeight\"] = (drug_pop[\"Total_Weight\"] / drug_pop[\"Population\"]) * 100000"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "# export clean dataset to csv\n",
    "drug_pop.to_csv(\n",
    "    \"/Users/samsloate/Desktop/Data_Science/Opioids_Project/estimating-impact-of-opioids-2020-purlple-team/20_intermediate_files/drug_shipment_data.csv\"\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
