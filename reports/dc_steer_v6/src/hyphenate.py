"""Insert soft hyphens into long German compounds.

Chromium in this container ships no hyphenation dictionaries, so `hyphens: auto`
is a no-op and justified German text develops rivers around 20+ character
compounds. A curated dictionary is used instead of a rule-based hyphenator:
a wrong break point is worse than no break at all.

Only text nodes are touched -- never markup, and never the contents of
<pre>, <code>, <span class="ref"> or <title>.
"""
import re

SHY = "­"

# word -> break points marked with "-" (kept exactly as authored)
WORDS = """
Ab-stim-mungs-ar-beit Ab-bruch-kri-te-ri-um Ab-hän-gig-keit Ab-hän-gig-kei-ten
Ak-tua-li-sie-rung Ak-tua-li-sie-run-gen Ak-tua-li-sie-rungs-rich-tun-gen
Ak-ti-vie-rungs-funk-ti-on An-fangs-lern-ra-te An-for-de-run-gen
An-wen-dungs-re-port An-wen-dungs-fall An-wen-dungs-fäl-le
Auf-ga-ben-be-schrei-bung Auf-ga-ben-in-stanz Auf-ga-ben-stel-lung
Aus-ga-be-di-men-sio-nen Aus-ga-be-ele-men-te Aus-ga-be-schicht
Aus-gangs-di-men-si-on Aus-gangs-di-men-sio-nen Aus-gangs-schicht
Be-schleu-ni-gung Be-schleu-ni-gungs-fak-tor Be-rech-nung Be-rech-nun-gen
Be-wer-tungs-maß-stab Bench-mark-er-geb-nis-se Bench-mark-lauf
Code-ba-sis Code-du-pli-ka-ti-on Du-pli-ka-ti-on
Da-ten-auf-be-rei-tung De-ter-mi-nis-mus de-ter-mi-nis-tisch
Ein-gangs-di-men-si-on Ein-stel-lun-gen Ein-stiegs-funk-ti-on Ein-zel-lauf
Emp-feh-lung Emp-feh-lun-gen En-er-gie-ar-bi-tra-ge Ent-wick-lungs-ge-schich-te
Ent-wick-lungs-pfad Er-satz-pa-ra-me-ter Er-war-tungs-wert
Ex-pe-ri-ment Ex-pe-ri-men-te ex-pe-ri-men-tell
Fall-un-ter-schei-dung Feh-ler-be-hand-lung
Ge-nau-ig-keits-an-for-de-rung Ge-ne-ra-li-sie-rung Ge-ne-ra-li-sie-rungs-lü-cke
Ge-gen-über-stel-lung Ge-samt-schritt-zahl Ge-stal-tungs-raum
Gleit-kom-ma-arith-me-tik Gra-di-en-ten-ab-stieg Gra-di-en-ten-ab-stiegs-ver-fah-ren
Gra-di-en-ten-rau-schen Gra-di-en-ten-schät-zer Gra-di-en-ten-va-ri-anz
Grund-la-gen Her-aus-for-de-rung Her-aus-for-de-run-gen
Hilfs-funk-tio-nen Hy-per-graph-par-ti-tio-nie-rung
Hy-per-pa-ra-me-ter Hy-per-pa-ra-me-tern Hy-per-pa-ra-me-ters
Hy-per-pa-ra-me-ter-op-ti-mie-rung Hy-per-pa-ra-me-ter-raum Hy-per-pa-ra-me-ter-satz
Im-ple-men-tie-rung Im-ple-men-tie-run-gen Im-ple-men-tie-rungs-auf-wand
in-stru-men-tier-ten in-te-res-san-te in-te-res-san-tes-te
Ka-li-brie-rung Nach-ka-li-brie-rung Kom-po-nen-te Kom-po-nen-ten
Kon-fi-gu-ra-ti-on Kon-fi-gu-ra-tio-nen Kon-fi-gu-ra-ti-ons-raum
Kon-ver-genz Kon-ver-genz-ra-te Kon-ver-genz-ver-hal-ten
Kor-rek-tur-term Kor-rek-tu-ren Krüm-mungs-be-gren-zung
Lern-ra-te Lern-ra-ten Lern-ra-ten-plan Li-te-ra-tur Li-te-ra-tur-stel-le
ma-ni-pu-lier-ba-res Maß-stabs-kor-rek-tur mehr-schich-ti-ges
Mess-feh-ler Mes-sun-gen Mess-rau-schen Mi-ni-batch Mi-ni-bat-ches
Mi-schungs-ge-wich-te Nach-kom-ma-stel-le Nach-kom-ma-stel-len
Nach-voll-zieh-bar-keit neu-ro-na-le neu-ro-na-len neu-ro-na-les
Nor-ma-li-sie-rung Op-ti-mie-rer-zu-stand Op-ti-mie-rer-zu-stands
Op-ti-mie-rungs-al-go-rith-mus Op-ti-mie-rungs-pro-blem Op-ti-mie-rungs-ver-fah-ren
Or-tho-go-na-li-sie-rung Pa-ra-me-ter-ak-tua-li-sie-rung Pa-ra-me-ter-grup-pe
Pa-ra-me-ter-grup-pen Pa-ra-me-ter-ten-sor Pa-ra-me-ter-ten-so-ren Pa-ra-me-ter-vek-tor
Pro-duk-tiv-ein-satz Punkt-schät-zung Rausch-bo-den Rausch-ni-veau Rausch-va-ri-anz
Re-chen-auf-wand Re-chen-bud-get Re-chen-zeit Re-fe-renz-im-ple-men-tie-rung
Re-gres-si-ons-ko-ef-fi-zi-ent Re-gres-si-ons-pro-blem Re-gu-la-ri-sie-rung
Re-pro-du-zier-bar-keit Ro-bust-heit Ruck-sack-pro-blem Rück-stands-puf-fer
Rück-wärts-durch-lauf Run-dungs-feh-ler Schätz-feh-ler Schätz-funk-ti-on
Schritt-funk-ti-on Schwie-rig-keits-grad Schwie-rig-keits-git-ter
Schwie-rig-keits-pa-ra-me-ter Si-gni-fi-kanz si-gni-fi-kant Ska-lier-bar-keit
Spei-cher-band-brei-te Spe-zia-li-sie-rung Stan-dard-ab-wei-chung
Steue-rungs-me-cha-nis-mus Stich-pro-ben-rau-schen
Trai-nings-bud-get Trai-nings-da-ten Trai-nings-lauf Trai-nings-läu-fe
Trai-nings-schlei-fe Trai-nings-zie-len Über-an-pas-sung Über-trag-bar-keit
Va-li-die-rungs-da-ten Va-li-die-rungs-kur-ve Va-li-die-rungs-men-ge
Va-li-die-rungs-ver-lauf Va-li-die-rungs-ver-lust Va-ri-anz-re-duk-ti-on
ver-all-ge-mei-nert ver-all-ge-mei-ner-te ver-all-ge-mei-ner-tes
Ver-all-ge-mei-ner-bar-keit Ver-gleichs-mes-sung Ver-lust-funk-ti-on Ver-zer-rung
Ver-öf-fent-li-chung Ver-öf-fent-li-chun-gen Ver-trau-ens-gren-zen
vor-kon-di-tio-nier-ter vor-kon-di-tio-nier-te Vor-wärts-durch-lauf
Vor-aus-set-zun-gen Vor-zei-chen-quan-ti-sie-rung Vor-zei-chen-schritt
Wahr-schein-lich-keit Wahr-schein-lich-keits-ver-tei-lung Wart-bar-keit
wei-ter-ent-wi-ckeln Wei-ter-ent-wick-lung Wei-ter-ent-wick-lun-gen
Ver-gleich-bar-keit Wett-be-werb Wett-be-werbs-vor-teil Wie-der-hol-bar-keit Wie-der-ver-wend-bar-keit
wirt-schaft-li-ches Zer-brech-lich-keit Ziel-funk-ti-on
zu-sam-men-ge-hal-ten Zu-sam-men-fas-sung zwei-di-men-sio-na-les zwei-di-men-sio-na-le
zwi-schen-ge-spei-cher-te zwi-schen-ge-spei-cher-tes Zwi-schen-er-geb-nis
Zwi-schen-er-geb-nis-se Zwi-schen-schicht
auf-schluss-rei-ches auf-schluss-reich
hand-ge-schrie-be-ne hand-ge-schrie-be-nen hand-ge-schrie-be-ner hand-ge-schrie-ben
Ab-bruch-me-cha-nis-mus Ab-bruch-zeit-punkt Ab-stim-mungs-er-geb-nis
Ab-stim-mungs-er-geb-nis-se An-fangs-ge-wich-te Auf-ga-ben-aus-nut-zung
Aus-füh-rungs-um-ge-bung Aus-ga-be-di-men-si-on Aus-stiegs-kri-te-ri-um
Aus-wer-tungs-mo-dus Bei-trags-ver-zeich-nis Bench-mark-vor-sprung
Be-wer-tungs-lo-gik Be-wer-tungs-punkt Block-er-geb-nis-se
dif-fe-renz-ba-siert dif-fe-renz-ba-sier-te dif-fe-renz-ba-sier-ter
ein-ge-schwun-ge-nen Ein-rei-chungs-an-ga-ben epo-chen-kon-stant
Funk-ti-ons-än-de-rung Ge-schwin-dig-keit Ge-wichts-ma-tri-zen
Ge-wichts-mit-te-lung Gleit-kom-ma-ad-di-ti-on Gleit-kom-ma-drift
gra-di-en-ten-ba-sier-te Gra-di-en-ten-schritt Gra-di-en-ten-schät-zung
her-aus-ge-rech-net her-aus-nor-mie-ren In-dex-arith-me-tik In-dex-gleich-heit
In-itia-li-sie-rung Kan-di-da-ten-lis-te krüm-mungs-ba-sier-ten
krüm-mungs-ge-trie-be-nen Lauf-sta-tis-ti-ken Mi-ni-mal-norm-lö-sung
mo-men-tum-ba-sier-ten mo-men-tum-ge-trie-be-nen Nach-prüf-bar-keit
nach-rich-ten-tech-ni-schen nach-voll-zieh-bar Ne-ben-dia-go-na-len
neu-tra-li-sie-ren-den Nor-mie-rungs-grö-ßen Op-ti-mie-rer-bau-stei-ne
Op-ti-mie-rer-fort-schritt Op-ti-mie-rer-lo-gik Op-ti-mie-rer-schnitt-stel-le
Op-ti-mie-rungs-rich-tung or-tho-go-na-li-siert Pa-ra-me-ter-än-de-rung
Pa-ra-me-ter-sät-zen Prä-fix-sum-men-ta-bel-le Pro-gno-se-rech-nung
quan-ti-fi-zier-bar Re-gres-si-ons-auf-ga-ben re-pro-du-zier-ba-re
Schritt-auf-lö-sung Schwes-ter-al-go-rith-mus selbst-be-züg-li-cher
Selbst-ein-stel-lung Selbst-ein-stel-lungs-lauf Si-cher-heits-ar-gu-men-ta-ti-on
Ska-len-pa-ra-me-ter Sta-gna-ti-ons-zäh-ler Stei-gungs-glät-tung
Stich-pro-ben-um-fang tie-fen-ab-hän-gi-ge tie-fen-un-ab-hän-gig
Track-da-tei-na-men Trai-nings-kos-ten Trai-nings-pha-sen Trai-nings-punk-te
Trai-nings-schrit-te Un-gleich-ver-tei-lung un-miss-ver-ständ-lich
un-ter-schied-lich un-ter-schied-li-che Va-li-die-rungs-zeit-punkt
va-ri-anz-re-du-zier-te Va-ri-anz-schät-zer ver-all-ge-mei-nern
Ver-hal-tens-än-de-rung ver-hal-tens-neu-tral Ver-stär-kungs-fak-tor
Ver-suchs-pla-nung Ver-trau-ens-gat-ter vor-ge-schal-te-ter
vor-ge-schla-ge-nen Vor-wärts-durch-läu-fe Vor-zei-chen-über-ein-stim-mung
Vor-zei-chen-wi-der-spruch wei-ter-ver-wen-den Zu-falls-pro-jek-ti-on
Zu-falls-vek-to-ren zu-sam-men-ge-fasst Lauf-zeit-si-gna-tur Ar-beits-pa-ke-te Dif-fe-renz-schät-zer Höchst-punkt-zahl in-stru-men-tier-te
Stan-dard-nor-mal-ver-teil-te Schwan-kungs-brei-te An-nah-me-gren-ze
"""

def _flip(w):
    """The other capitalisation of a word's first letter."""
    return (w[0].lower() + w[1:]) if w[:1].isupper() else (w[0].upper() + w[1:])


_PAIRS = []
for token in WORDS.split():
    plain = token.replace("-", "")
    soft = token.replace("-", SHY)
    _PAIRS.append((plain, soft))
    if _flip(plain) != plain:
        _PAIRS.append((_flip(plain), _flip(soft)))
# longest first so "Hyperparameteroptimierung" wins over "Hyperparameter"
_PAIRS.sort(key=lambda p: -len(p[0]))

_SKIP = re.compile(r"(<pre\b.*?</pre>|<code\b.*?</code>|<script\b.*?</script>"
                   r"|<style\b.*?</style>|<title\b.*?</title>"
                   r'|<span class="ref">.*?</span>|<[^>]+>|&[a-zA-Z#0-9]+;)',
                   re.S)


def _apply(text):
    for plain, soft in _PAIRS:
        if plain in text:
            text = text.replace(plain, soft)
    return text


def hyphenate(html):
    out, last = [], 0
    for m in _SKIP.finditer(html):
        out.append(_apply(html[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(_apply(html[last:]))
    return "".join(out)
