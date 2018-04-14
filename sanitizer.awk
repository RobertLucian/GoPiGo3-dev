BEGIN { RS="^$"; ORS="" }
{
    gsub(/@/,"@A")
    gsub(/\\"/,"@B")
    nf = patsplit($0,flds,/"[^"]*"/,seps)
    $0 = ""
    for (i=0; i<=nf; i++) {
        $0 = $0 gensub(/\s*\n\s*/," ","g",flds[i]) seps[i]
    }
    gsub(/@B/,"\\\"")
    gsub(/@A/,"@")
    print
}
