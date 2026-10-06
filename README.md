# myls

Bir klasördeki dosyaları listeleyen, filtreleme, sıralama ve renk/ikon seçenekleri olan basit bir komut satırı aracı.

## Kurulum

```bash
git clone https://github.com/S1aken/ls.git
cd ls
pip install -e .
```

Kurulumdan sonra terminalde `myls` komutu kullanılabilir.

## Hızlı başlangıç

```bash
myls                  # bulunduğun klasörü listeler
myls C:\Users\TR      # verdiğin klasörü listeler
```

Hiçbir seçenek vermezsen gizli dosyalar gösterilmez, liste isme göre sıralanır, çıktı düz yazı olur.

## Seçenekler

| Seçenek | Değerler | Varsayılan | Ne yapar |
|---|---|---|---|
| `--filter` | `visible`, `all`, `files`, `dirs` | `visible` | Neyin listeleneceğini seçer |
| `--sort` | `name`, `size`, `date` | `name` | Sıralama ölçütünü seçer |
| `--style` | `plain`, `color`, `icons` | `plain` | Çıktının görünümünü seçer |
| `--color` | `blue`, `red`, `green`, `yellow` | `blue` | `--style color` için rengi seçer |

### `--filter` değerleri

| Değer | Sonuç |
|---|---|
| `visible` | Gizli olmayan her şey (dosya + klasör) |
| `all` | Gizli dosyalar (`.git` gibi) dahil her şey |
| `files` | Sadece dosyalar |
| `dirs` | Sadece klasörler |

### `--sort` değerleri

| Değer | Sonuç |
|---|---|
| `name` | İsme göre, A'dan Z'ye |
| `size` | Boyuta göre, küçükten büyüğe |
| `date` | Değiştirilme tarihine göre, eskiden yeniye |

### `--style` değerleri

| Değer | Sonuç |
|---|---|
| `plain` | Düz yazı |
| `color` | Klasörler renkli, dosyalar normal |
| `icons` | Klasörlerin başında 📁, dosyaların başında 📄 |

## Örnekler

Her şeyi göster, gizli dosyalar dahil:

```bash
myls --filter all
```

Sadece klasörleri göster:

```bash
myls --filter dirs
```

Sadece dosyaları boyuta göre sırala:

```bash
myls --filter files --sort size
```

En son değiştirilen dosya en altta olsun:

```bash
myls --filter files --sort date
```

Klasörleri kırmızı göster:

```bash
myls --style color --color red
```

İkonlu liste:

```bash
myls --style icons
```

Hepsini birlikte kullan: sadece dosyalar, boyuta göre sıralı, ikonlu:

```bash
myls --filter files --sort size --style icons
```

Başka bir klasörde, gizliler dahil, tarihe göre sıralı:

```bash
myls C:\Users\TR\Desktop --filter all --sort date
```

## İyi bilinmesi gerekenler

- Seçeneklerin yazılma sırası önemli değildir. `myls --sort size --filter files` ile `myls --filter files --sort size` aynı sonucu verir.
- `--color` sadece `--style color` ile birlikte etkilidir. `--style icons` ile kullanılırsa yok sayılır.
- `--style color` yalnızca klasörleri boyar, dosyalar normal renkte kalır.
- Klasörlerin boyutu, içindeki dosyaların toplamı değildir. Klasörün kendi kayıt boyutudur (Windows'ta genelde 0 görünür). `--sort size` en anlamlı sonucu `--filter files` ile verir.
- Var olmayan bir klasör verirsen şu hatayı alırsın: `No such directory: '...'`.
- Geçersiz bir değer yazarsan (örneğin `--sort weight`) araç seçenekleri listeleyen bir hata mesajı verir.

## Yardım

```bash
myls --help
```

## Testleri çalıştırma

```bash
pip install pytest
pytest -q
```
