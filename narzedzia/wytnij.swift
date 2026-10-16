// Wycina osobę ze zdjęcia (Vision, macOS 14+) i zapisuje PNG z przezroczystym tłem.
// Na standardowe wyjście wypisuje prostokąt twarzy w pikselach: x y szer wys (początek u góry z lewej).
// Użycie: swift wytnij.swift wejście.jpg wyjście.png
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count == 3, let wejscie = CIImage(contentsOf: URL(fileURLWithPath: args[1])) else {
    FileHandle.standardError.write("Użycie: swift wytnij.swift wejście wyjście.png\n".data(using: .utf8)!)
    exit(1)
}

let handler = VNImageRequestHandler(ciImage: wejscie)
let maska = VNGenerateForegroundInstanceMaskRequest()
let twarze = VNDetectFaceRectanglesRequest()
try handler.perform([maska, twarze])

guard let wynik = maska.results?.first else {
    FileHandle.standardError.write("Nie znaleziono osoby\n".data(using: .utf8)!)
    exit(2)
}
let bufor = try wynik.generateMaskedImage(ofInstances: wynik.allInstances, from: handler, croppedToInstancesExtent: false)
let wyciete = CIImage(cvPixelBuffer: bufor)

let ctx = CIContext()
guard let cg = ctx.createCGImage(wyciete, from: wyciete.extent) else { exit(3) }
let rep = NSBitmapImageRep(cgImage: cg)
try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))

let W = wejscie.extent.width, H = wejscie.extent.height
if let t = (twarze.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }) {
    let b = t.boundingBox
    print(Int(b.minX * W), Int((1 - b.maxY) * H), Int(b.width * W), Int(b.height * H))
} else {
    print("brak")
}
