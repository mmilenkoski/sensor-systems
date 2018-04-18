konsenzus <- function(tabela, s, l){
  t <- nrow(tabela)
  matricaPoramnuvanje <- matrix("0", t, l)
  for (i in 1:t){
    matricaPoramnuvanje[i, ] = tabela[i, s[i]:(s[i]+l-1)]
  }
  print(matricaPoramnuvanje)
  profilnaMatrica <- matrix(0, 4, l, dimnames = list(c("A", "C", "G", "T"), NULL))
  skor = 0
  konsenzusString = c()
  for(i in 1:l){
    maks = 0
    maksBukva = "A"
    for(j in 1:t){
      bukva <- matricaPoramnuvanje[j, i]
      profilnaMatrica[bukva, i] <- profilnaMatrica[bukva, i] + 1
      if(profilnaMatrica[bukva, i] > maks){
        maks = profilnaMatrica[bukva, i]
        maksBukva = bukva
      }
    }
    skor = skor + maks
    konsenzusString = c(konsenzusString, maksBukva)
  }
  print(profilnaMatrica)
  print(skor[[1]])
  print(konsenzusString)
}

main <- function(){
  s1 <- "AAGGAGAGACCGCCTTCCCCGCCATGAAGTTCGAGAGGCAGCACATGGACAGCGGCAGCACCAGCAG"
  s1 <- strsplit(s1, split='')[[1]]
  s2 <- "AGCAACCCCACCTACTGCTGCGGCTAAACCAGATGATGAAGAGGAGGAACATGACCCAGGGCTGGTG"
  s2 <- strsplit(s2, split='')[[1]]
  s3 <- "AAGTCGGCTAACCCGTGAACACCTTCGTGCACGAGCCCCTGGCCGACGTGCAGGCCATCTGCCTGCA"
  s3 <- strsplit(s3, split='')[[1]]
  s4 <- "AAGAACATACCCTAGGCACCTGCAAGAACGGCCAGAGCAACTGCTACCAGAGCAGCAGCAGCATGCA"
  s4 <- strsplit(s4, split='')[[1]]
  s5 <- "ATCACCGACTGCAGGCTGACCAGCGGCAGCAAGTACCCCAACTGCCGGTGAGCGCCTACCAGACCAG"
  s5 <- strsplit(s5, split='')[[1]]
  s6 <- "CAGAAGGAGAGGCACATCATCGTGGCCTTCAAGCGAGCGAGGGCAACCCCTACGTGCCCGTGCACTT"
  s6 <- strsplit(s6, split='')[[1]]
  table = matrix("0", nrow=6, ncol=length(s1))
  table[1, ] <- s1
  table[2, ] <- s2
  table[3, ] <- s3
  table[4, ] <- s4
  table[5, ] <- s5
  table[6, ] <- s6
  s <- c(9, 19, 4, 9, 10, 16)
  l = 8
  konsenzus(table, s, l)
}