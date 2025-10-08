import Foundation
import Accelerate
import simd

// MARK: - Professional Audio Analysis Classes

struct SpectralFeatures {
    let centroid: Float
    let rolloff: Float
    let flux: Float
    let spread: Float
    let skewness: Float
    let kurtosis: Float
}

struct FrequencyBands {
    let subBass: Float    // 20-60 Hz
    let bass: Float       // 60-250 Hz
    let lowMid: Float     // 250-500 Hz
    let mid: Float        // 500-2000 Hz
    let highMid: Float    // 2000-4000 Hz
    let treble: Float     // 4000+ Hz
}

struct ProfessionalAudioAnalysis {
    let spectralFeatures: SpectralFeatures
    let frequencyBands: FrequencyBands
    let harmonicContent: HarmonicContent
    let rhythmAnalysis: RhythmAnalysis
    let dynamicRange: Float
    let peakLevel: Float
    let rmsLevel: Float
}

struct HarmonicContent {
    let fundamental: Float
    let harmonics: [Float]
    let inharmonicity: Float
    let spectralBrightness: Float
}

struct RhythmAnalysis {
    let tempo: Float
    let beatStrength: Float
    let rhythmComplexity: Float
    let syncopation: Float
}

class SpectralAnalyzer {
    private var previousMagnitudes: [Float] = []
    private let analysisWindowSize = 2048
    
    func analyze(fftData: [Float]) -> SpectralFeatures {
        let magnitudes = fftData.map { abs($0) }
        
        let centroid = calculateSpectralCentroid(magnitudes: magnitudes)
        let rolloff = calculateSpectralRolloff(magnitudes: magnitudes)
        let flux = calculateSpectralFlux(current: magnitudes)
        let spread = calculateSpectralSpread(magnitudes: magnitudes, centroid: centroid)
        let skewness = calculateSpectralSkewness(magnitudes: magnitudes, centroid: centroid)
        let kurtosis = calculateSpectralKurtosis(magnitudes: magnitudes, centroid: centroid)
        
        previousMagnitudes = magnitudes
        
        return SpectralFeatures(
            centroid: centroid,
            rolloff: rolloff,
            flux: flux,
            spread: spread,
            skewness: skewness,
            kurtosis: kurtosis
        )
    }
    
    private func calculateSpectralCentroid(magnitudes: [Float]) -> Float {
        var weightedSum: Float = 0.0
        var magnitudeSum: Float = 0.0
        
        for (index, magnitude) in magnitudes.enumerated() {
            let frequency = Float(index)
            weightedSum += frequency * magnitude
            magnitudeSum += magnitude
        }
        
        return magnitudeSum > 0 ? weightedSum / magnitudeSum : 0.0
    }
    
    private func calculateSpectralRolloff(magnitudes: [Float]) -> Float {
        let totalEnergy = magnitudes.reduce(0, +)
        let rolloffThreshold = totalEnergy * 0.85
        
        var cumulativeEnergy: Float = 0.0
        for (index, magnitude) in magnitudes.enumerated() {
            cumulativeEnergy += magnitude
            if cumulativeEnergy >= rolloffThreshold {
                return Float(index) / Float(magnitudes.count)
            }
        }
        
        return 1.0
    }
    
    private func calculateSpectralFlux(current: [Float]) -> Float {
        if previousMagnitudes.isEmpty {
            return 0.0
        }
        
        let minCount = min(current.count, previousMagnitudes.count)
        var flux: Float = 0.0
        
        for i in 0..<minCount {
            let diff = current[i] - previousMagnitudes[i]
            flux += max(0, diff) // Only positive changes
        }
        
        return flux / Float(minCount)
    }
    
    private func calculateSpectralSpread(magnitudes: [Float], centroid: Float) -> Float {
        var weightedSum: Float = 0.0
        var magnitudeSum: Float = 0.0
        
        for (index, magnitude) in magnitudes.enumerated() {
            let frequency = Float(index)
            let diff = frequency - centroid
            weightedSum += diff * diff * magnitude
            magnitudeSum += magnitude
        }
        
        return magnitudeSum > 0 ? sqrt(weightedSum / magnitudeSum) : 0.0
    }
    
    private func calculateSpectralSkewness(magnitudes: [Float], centroid: Float) -> Float {
        let spread = calculateSpectralSpread(magnitudes: magnitudes, centroid: centroid)
        guard spread > 0 else { return 0.0 }
        
        var weightedSum: Float = 0.0
        var magnitudeSum: Float = 0.0
        
        for (index, magnitude) in magnitudes.enumerated() {
            let frequency = Float(index)
            let normalizedDiff = (frequency - centroid) / spread
            weightedSum += normalizedDiff * normalizedDiff * normalizedDiff * magnitude
            magnitudeSum += magnitude
        }
        
        return magnitudeSum > 0 ? weightedSum / magnitudeSum : 0.0
    }
    
    private func calculateSpectralKurtosis(magnitudes: [Float], centroid: Float) -> Float {
        let spread = calculateSpectralSpread(magnitudes: magnitudes, centroid: centroid)
        guard spread > 0 else { return 0.0 }
        
        var weightedSum: Float = 0.0
        var magnitudeSum: Float = 0.0
        
        for (index, magnitude) in magnitudes.enumerated() {
            let frequency = Float(index)
            let normalizedDiff = (frequency - centroid) / spread
            let diff4 = normalizedDiff * normalizedDiff * normalizedDiff * normalizedDiff
            weightedSum += diff4 * magnitude
            magnitudeSum += magnitude
        }
        
        return magnitudeSum > 0 ? weightedSum / magnitudeSum : 0.0
    }
}

class BeatDetector {
    private var energyHistory: [Float] = []
    private var beatTimes: [Double] = []
    private let historyLength = 43 // ~1 second at 44.1kHz
    private let thresholdMultiplier: Float = 1.3
    
    func detectBeat(currentFFT: [Float], previousFFT: [Float]) -> Bool {
        let currentEnergy = calculateEnergy(fftData: currentFFT)
        let previousEnergy = calculateEnergy(fftData: previousFFT)
        
        energyHistory.append(currentEnergy)
        if energyHistory.count > historyLength {
            energyHistory.removeFirst()
        }
        
        guard energyHistory.count >= historyLength else { return false }
        
        let averageEnergy = energyHistory.reduce(0, +) / Float(energyHistory.count)
        let variance = calculateVariance(values: energyHistory, mean: averageEnergy)
        let threshold = averageEnergy + (variance * thresholdMultiplier)
        
        let beatDetected = currentEnergy > threshold && currentEnergy > previousEnergy
        
        if beatDetected {
            beatTimes.append(CACurrentMediaTime())
        }
        
        return beatDetected
    }
    
    func calculateTempo() -> Float {
        guard beatTimes.count >= 2 else { return 0.0 }
        
        let recentBeats = Array(beatTimes.suffix(8)) // Last 8 beats
        var intervals: [Double] = []
        
        for i in 1..<recentBeats.count {
            intervals.append(recentBeats[i] - recentBeats[i-1])
        }
        
        let averageInterval = intervals.reduce(0, +) / Double(intervals.count)
        let tempo = 60.0 / averageInterval // BPM
        
        return Float(max(60.0, min(200.0, tempo))) // Clamp to reasonable range
    }
    
    private func calculateEnergy(fftData: [Float]) -> Float {
        return fftData.reduce(0) { $0 + $1 * $1 }
    }
    
    private func calculateVariance(values: [Float], mean: Float) -> Float {
        let squaredDiffs = values.map { ($0 - mean) * ($0 - mean) }
        return squaredDiffs.reduce(0, +) / Float(values.count)
    }
}

class HarmonicAnalyzer {
    func analyze(fftData: [Float]) -> HarmonicContent {
        let fundamental = detectFundamental(fftData: fftData)
        let harmonics = extractHarmonics(fftData: fftData, fundamental: fundamental)
        let inharmonicity = calculateInharmonicity(harmonics: harmonics, fundamental: fundamental)
        let spectralBrightness = calculateSpectralBrightness(fftData: fftData)
        
        return HarmonicContent(
            fundamental: fundamental,
            harmonics: harmonics,
            inharmonicity: inharmonicity,
            spectralBrightness: spectralBrightness
        )
    }
    
    private func detectFundamental(fftData: [Float]) -> Float {
        // Find the lowest significant peak
        var maxMagnitude: Float = 0.0
        var fundamentalIndex = 0
        
        for i in 10..<fftData.count/4 { // Avoid DC and very high frequencies
            if fftData[i] > maxMagnitude {
                maxMagnitude = fftData[i]
                fundamentalIndex = i
            }
        }
        
        return Float(fundamentalIndex) / Float(fftData.count)
    }
    
    private func extractHarmonics(fftData: [Float], fundamental: Float) -> [Float] {
        let fundamentalIndex = Int(fundamental * Float(fftData.count))
        var harmonics: [Float] = []
        
        for harmonic in 2...10 { // Extract first 10 harmonics
            let harmonicIndex = fundamentalIndex * harmonic
            if harmonicIndex < fftData.count {
                harmonics.append(fftData[harmonicIndex])
            } else {
                harmonics.append(0.0)
            }
        }
        
        return harmonics
    }
    
    private func calculateInharmonicity(harmonics: [Float], fundamental: Float) -> Float {
        // Calculate deviation from perfect harmonic ratios
        var totalDeviation: Float = 0.0
        var validHarmonics = 0
        
        for (index, harmonic) in harmonics.enumerated() {
            if harmonic > 0.1 { // Only consider significant harmonics
                let expectedRatio = Float(index + 2) // 2nd, 3rd, 4th harmonic, etc.
                let actualRatio = harmonic / fundamental
                let deviation = abs(actualRatio - expectedRatio) / expectedRatio
                totalDeviation += deviation
                validHarmonics += 1
            }
        }
        
        return validHarmonics > 0 ? totalDeviation / Float(validHarmonics) : 0.0
    }
    
    private func calculateSpectralBrightness(fftData: [Float]) -> Float {
        let midPoint = fftData.count / 2
        let lowFreqEnergy = Array(fftData[0..<midPoint]).reduce(0, +)
        let highFreqEnergy = Array(fftData[midPoint..<fftData.count]).reduce(0, +)
        
        let totalEnergy = lowFreqEnergy + highFreqEnergy
        return totalEnergy > 0 ? highFreqEnergy / totalEnergy : 0.0
    }
}

// MARK: - Professional Audio Analysis Extensions

extension AudioEngine {
    
    func calculateProfessionalFrequencyBands(fftResult: [Float]) -> FrequencyBands {
        let sampleRate: Float = 44100.0
        let nyquist = sampleRate / 2.0
        let binSize = nyquist / Float(fftResult.count)
        
        // Define frequency ranges in Hz
        let subBassEnd = 60.0
        let bassEnd = 250.0
        let lowMidEnd = 500.0
        let midEnd = 2000.0
        let highMidEnd = 4000.0
        
        let subBassStart = 20.0
        let bassStart = subBassEnd
        let lowMidStart = bassEnd
        let midStart = lowMidEnd
        let highMidStart = midEnd
        let trebleStart = highMidEnd
        
        let subBass = calculateBandEnergy(fftResult: fftResult, startFreq: subBassStart, endFreq: subBassEnd, binSize: binSize)
        let bass = calculateBandEnergy(fftResult: fftResult, startFreq: bassStart, endFreq: bassEnd, binSize: binSize)
        let lowMid = calculateBandEnergy(fftResult: fftResult, startFreq: lowMidStart, endFreq: lowMidEnd, binSize: binSize)
        let mid = calculateBandEnergy(fftResult: fftResult, startFreq: midStart, endFreq: midEnd, binSize: binSize)
        let highMid = calculateBandEnergy(fftResult: fftResult, startFreq: highMidStart, endFreq: highMidEnd, binSize: binSize)
        let treble = calculateBandEnergy(fftResult: fftResult, startFreq: trebleStart, endFreq: nyquist, binSize: binSize)
        
        return FrequencyBands(
            subBass: subBass,
            bass: bass,
            lowMid: lowMid,
            mid: mid,
            highMid: highMid,
            treble: treble
        )
    }
    
    private func calculateBandEnergy(fftResult: [Float], startFreq: Double, endFreq: Double, binSize: Float) -> Float {
        let startBin = Int(startFreq / Double(binSize))
        let endBin = Int(endFreq / Double(binSize))
        
        let clampedStartBin = max(0, min(startBin, fftResult.count - 1))
        let clampedEndBin = max(clampedStartBin, min(endBin, fftResult.count - 1))
        
        let bandData = Array(fftResult[clampedStartBin...clampedEndBin])
        return bandData.reduce(0, +) / Float(bandData.count)
    }
    
    func applyAWeighting(bands: FrequencyBands) -> FrequencyBands {
        // A-weighting coefficients for each frequency band
        let subBassWeight: Float = 0.1
        let bassWeight: Float = 0.3
        let lowMidWeight: Float = 0.6
        let midWeight: Float = 1.0
        let highMidWeight: Float = 0.8
        let trebleWeight: Float = 0.4
        
        return FrequencyBands(
            subBass: bands.subBass * subBassWeight,
            bass: bands.bass * bassWeight,
            lowMid: bands.lowMid * lowMidWeight,
            mid: bands.mid * midWeight,
            highMid: bands.highMid * highMidWeight,
            treble: bands.treble * trebleWeight
        )
    }
}
